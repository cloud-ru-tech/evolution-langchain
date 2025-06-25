Управление токенами
===================

Этот раздел содержит подробное руководство по автоматическому управлению токенами в Evolution LangChain.

Автоматическое управление
-------------------------

Токены управляются автоматически без вмешательства пользователя:

.. code-block:: python

    from evolution_langchain import EvolutionInference

    # Токены управляются автоматически
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    # При первом запросе автоматически получается токен
    response = llm.invoke("Привет!")

Жизненный цикл токена
---------------------

1. **Получение**: При первом API запросе автоматически выполняется аутентификация
2. **Кэширование**: Токен сохраняется в памяти
3. **Мониторинг**: Постоянная проверка времени истечения
4. **Обновление**: Автоматическое обновление за 30 секунд до истечения
5. **Повтор**: Цикл повторяется для поддержания актуальности

Особенности реализации
----------------------

Буферизация времени
~~~~~~~~~~~~~~~~~~~

Токен обновляется за 30 секунд до истечения:

.. code-block:: python

    REFRESH_BUFFER_SECONDS = 30

Это предотвращает ошибки из-за истёкших токенов и обеспечивает бесперебойную работу.

Thread-safety
~~~~~~~~~~~~~

Все операции с токенами thread-safe благодаря использованию блокировок:

.. code-block:: python

    import threading

    # Внутри TokenManager
    self._lock = threading.Lock()

    def get_token(self) -> str:
        with self._lock:
            if self._is_token_expired():
                self._refresh_token()
            return self._token

Обработка ошибок
~~~~~~~~~~~~~~~~

При ошибках аутентификации выбрасывается ``RuntimeError``:

.. code-block:: python

    try:
        response = llm.invoke("Тест")
    except RuntimeError as e:
        print(f"Ошибка аутентификации: {e}")
        # Возможные причины:
        # - Неверные key_id/secret  
        # - Проблемы с сетью
        # - Недоступность auth сервера

Конфигурация аутентификации
---------------------------

Альтернативный auth URL
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        auth_url="https://custom-auth-server.com/api/v1/token"
    )

Использование переменных окружения
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    export EVOLUTION_KEY_ID="your-key-id"
    export EVOLUTION_SECRET="your-secret"
    export EVOLUTION_TOKEN_URL="https://custom-auth-server.com/api/v1/token"

.. code-block:: python

    import os

    llm = EvolutionInference(
        model="your-model",
        key_id=os.getenv("EVOLUTION_KEY_ID"),
        secret=os.getenv("EVOLUTION_SECRET"),
        base_url="https://your-api-endpoint.com/v1",
        auth_url=os.getenv("EVOLUTION_TOKEN_URL")
    )

Мониторинг токенов
------------------

Логирование
~~~~~~~~~~~

Включите логирование для отладки:

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("evolution_langchain")

    # Теперь будут видны сообщения о получении и обновлении токенов

Метрики
~~~~~~~

Создайте wrapper для сбора метрик:

.. code-block:: python

    import time
    from dataclasses import dataclass

    @dataclass
    class TokenStats:
        total_refreshes: int = 0
        successful_refreshes: int = 0
        avg_refresh_time: float = 0.0

    class MonitoredEvolutionInference:
        def __init__(self, llm):
            self.llm = llm
            self.stats = TokenStats()
            
        def invoke(self, prompt):
            start_time = time.time()
            
            try:
                response = self.llm.invoke(prompt)
                
                # Обновить статистику
                self.stats.successful_refreshes += 1
                refresh_time = time.time() - start_time
                self._update_avg_time(refresh_time)
                    
                return response
            except Exception as e:
                self.stats.total_refreshes += 1
                raise
        
        def _update_avg_time(self, new_time):
            if self.stats.successful_refreshes == 1:
                self.stats.avg_refresh_time = new_time
            else:
                # Скользящее среднее
                self.stats.avg_refresh_time = (
                    (self.stats.avg_refresh_time * (self.stats.successful_refreshes - 1) + new_time) 
                    / self.stats.successful_refreshes
                )

Безопасность
------------

Защита учетных данных
~~~~~~~~~~~~~~~~~~~~~

Используйте переменные окружения для хранения секретов:

.. code-block:: python

    import os
    from dotenv import load_dotenv

    # Загрузка переменных из .env файла
    load_dotenv()

    llm = EvolutionInference(
        model=os.getenv("EVOLUTION_MODEL"),
        key_id=os.getenv("EVOLUTION_KEY_ID"),
        secret=os.getenv("EVOLUTION_SECRET"),
        base_url=os.getenv("EVOLUTION_BASE_URL")
    )

Ротация ключей
~~~~~~~~~~~~~~

Регулярно обновляйте ключи доступа:

.. code-block:: python

    class KeyRotationManager:
        def __init__(self, primary_key_id, primary_secret, 
                     backup_key_id, backup_secret):
            self.primary_key_id = primary_key_id
            self.primary_secret = primary_secret
            self.backup_key_id = backup_key_id
            self.backup_secret = backup_secret
            self.use_primary = True
        
        def get_current_credentials(self):
            if self.use_primary:
                return self.primary_key_id, self.primary_secret
            else:
                return self.backup_key_id, self.backup_secret
        
        def rotate_keys(self):
            self.use_primary = not self.use_primary
            print(f"Переключение на {'основной' if self.use_primary else 'резервный'} ключ")

    # Использование
    key_manager = KeyRotationManager(
        primary_key_id="primary-key",
        primary_secret="primary-secret",
        backup_key_id="backup-key",
        backup_secret="backup-secret"
    )

    key_id, secret = key_manager.get_current_credentials()
    llm = EvolutionInference(
        model="your-model",
        key_id=key_id,
        secret=secret,
        base_url="https://your-api-endpoint.com/v1"
    )

Обработка ошибок токенов
------------------------

Повторные попытки
~~~~~~~~~~~~~~~~~

Реализуйте механизм повторных попыток:

.. code-block:: python

    import time
    from evolution_langchain import EvolutionInference

    class RetryableEvolutionInference:
        def __init__(self, llm, max_retries=3, retry_delay=1):
            self.llm = llm
            self.max_retries = max_retries
            self.retry_delay = retry_delay
        
        def invoke(self, prompt):
            for attempt in range(self.max_retries):
                try:
                    return self.llm.invoke(prompt)
                except RuntimeError as e:
                    if "authentication" in str(e).lower() and attempt < self.max_retries - 1:
                        print(f"Ошибка аутентификации, попытка {attempt + 1}/{self.max_retries}")
                        time.sleep(self.retry_delay * (2 ** attempt))  # Экспоненциальная задержка
                    else:
                        raise e

    # Использование
    base_llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    retryable_llm = RetryableEvolutionInference(base_llm)

    try:
        response = retryable_llm.invoke("Привет!")
        print(response)
    except Exception as e:
        print(f"Все попытки не удались: {e}")

Fallback механизм
~~~~~~~~~~~~~~~~~

Реализуйте fallback на резервные ключи:

.. code-block:: python

    class FallbackEvolutionInference:
        def __init__(self, primary_llm, backup_llm):
            self.primary_llm = primary_llm
            self.backup_llm = backup_llm
            self.use_primary = True
        
        def invoke(self, prompt):
            try:
                if self.use_primary:
                    return self.primary_llm.invoke(prompt)
                else:
                    return self.backup_llm.invoke(prompt)
            except RuntimeError as e:
                if "authentication" in str(e).lower():
                    print("Переключение на резервный ключ")
                    self.use_primary = False
                    return self.backup_llm.invoke(prompt)
                else:
                    raise e

    # Создание основного и резервного LLM
    primary_llm = EvolutionInference(
        model="your-model",
        key_id="primary-key",
        secret="primary-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    backup_llm = EvolutionInference(
        model="your-model",
        key_id="backup-key",
        secret="backup-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    fallback_llm = FallbackEvolutionInference(primary_llm, backup_llm)

    # Использование
    response = fallback_llm.invoke("Привет!")

Полный пример
-------------

Объединение всех возможностей управления токенами:

.. code-block:: python

    import os
    import time
    import logging
    from dataclasses import dataclass
    from evolution_langchain import EvolutionInference

    @dataclass
    class TokenMetrics:
        total_requests: int = 0
        auth_errors: int = 0
        successful_refreshes: int = 0
        avg_response_time: float = 0.0

    class AdvancedTokenManager:
        def __init__(self, model, key_id, secret, base_url, 
                     backup_key_id=None, backup_secret=None):
            self.model = model
            self.key_id = key_id
            self.secret = secret
            self.base_url = base_url
            self.backup_key_id = backup_key_id
            self.backup_secret = backup_secret
            
            self.metrics = TokenMetrics()
            self.use_primary = True
            
            # Настройка логирования
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
            
            # Создание основного LLM
            self.primary_llm = EvolutionInference(
                model=model,
                key_id=key_id,
                secret=secret,
                base_url=base_url
            )
            
            # Создание резервного LLM если есть резервные ключи
            if backup_key_id and backup_secret:
                self.backup_llm = EvolutionInference(
                    model=model,
                    key_id=backup_key_id,
                    secret=backup_secret,
                    base_url=base_url
                )
            else:
                self.backup_llm = None
        
        def invoke(self, prompt, max_retries=3):
            self.metrics.total_requests += 1
            
            for attempt in range(max_retries):
                start_time = time.time()
                
                try:
                    # Выбор LLM
                    current_llm = self.primary_llm if self.use_primary else self.backup_llm
                    
                    if current_llm is None:
                        raise RuntimeError("Нет доступных LLM")
                    
                    response = current_llm.invoke(prompt)
                    
                    # Обновление метрик
                    response_time = time.time() - start_time
                    self._update_avg_time(response_time)
                    
                    self.logger.info(f"Запрос выполнен за {response_time:.2f}с")
                    return response
                    
                except RuntimeError as e:
                    response_time = time.time() - start_time
                    self.metrics.auth_errors += 1
                    
                    if "authentication" in str(e).lower():
                        self.logger.warning(f"Ошибка аутентификации, попытка {attempt + 1}/{max_retries}")
                        
                        # Переключение на резервный ключ
                        if self.backup_llm and self.use_primary:
                            self.logger.info("Переключение на резервный ключ")
                            self.use_primary = False
                            continue
                        
                        # Повторная попытка с задержкой
                        if attempt < max_retries - 1:
                            delay = 2 ** attempt
                            self.logger.info(f"Ожидание {delay}с перед повторной попыткой")
                            time.sleep(delay)
                            continue
                    
                    self.logger.error(f"Ошибка запроса: {e}")
                    raise e
        
        def _update_avg_time(self, new_time):
            if self.metrics.total_requests == 1:
                self.metrics.avg_response_time = new_time
            else:
                self.metrics.avg_response_time = (
                    (self.metrics.avg_response_time * (self.metrics.total_requests - 1) + new_time) 
                    / self.metrics.total_requests
                )
        
        def get_stats(self):
            return {
                "total_requests": self.metrics.total_requests,
                "auth_errors": self.metrics.auth_errors,
                "success_rate": ((self.metrics.total_requests - self.metrics.auth_errors) 
                                / self.metrics.total_requests * 100),
                "avg_response_time": self.metrics.avg_response_time,
                "using_primary": self.use_primary
            }

    def main():
        print("🚀 Evolution LangChain - Управление токенами")
        print("=" * 50)

        # Создание менеджера токенов
        token_manager = AdvancedTokenManager(
            model=os.getenv("EVOLUTION_MODEL", "your-model"),
            key_id=os.getenv("EVOLUTION_KEY_ID", "your-key-id"),
            secret=os.getenv("EVOLUTION_SECRET", "your-secret"),
            base_url=os.getenv("EVOLUTION_BASE_URL", "https://your-api-endpoint.com/v1"),
            backup_key_id=os.getenv("EVOLUTION_BACKUP_KEY_ID"),
            backup_secret=os.getenv("EVOLUTION_BACKUP_SECRET")
        )

        print("✅ Менеджер токенов инициализирован")
        print()

        # Выполнение запросов
        questions = [
            "Что такое Python?",
            "Объясни машинное обучение",
            "Что такое нейронные сети?"
        ]

        for i, question in enumerate(questions, 1):
            print(f"Запрос {i}: {question}")
            try:
                response = token_manager.invoke(question)
                print(f"Ответ: {response[:100]}...")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            print()

        # Вывод статистики
        stats = token_manager.get_stats()
        print("📊 Статистика:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    if __name__ == "__main__":
        main()

Что дальше?
-----------

- Изучите :doc:`error-handling` для детальной обработки ошибок
- Прочитайте :doc:`langchain-integration` для интеграции с LangChain
- Посмотрите :doc:`../api/token-manager` для документации API 