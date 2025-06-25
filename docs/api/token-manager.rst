TokenManager
============

.. automodule:: evolution_langchain.evolution_inference
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Обзор
-----

Класс ``TokenManager`` управляет жизненным циклом токенов доступа для Evolution Inference API. Обычно вам не нужно взаимодействовать с этим классом напрямую, так как ``EvolutionInference`` использует его автоматически.

Основные возможности
--------------------

- 🔐 **Автоматическая аутентификация**: Получение токенов по key_id и secret
- 🔄 **Автоматическое обновление**: Токены обновляются за 30 секунд до истечения
- 💾 **Кэширование**: Токены хранятся в памяти для повторного использования
- 🧵 **Thread-safety**: Безопасная работа в многопоточной среде
- ⚡ **Оптимизация**: Минимальное количество запросов на аутентификацию

Инициализация
-------------

.. code-block:: python

    from evolution_langchain.evolution_inference import TokenManager

    manager = TokenManager(
        key_id="your-key-id",
        secret="your-secret",
        auth_url="https://iam.api.cloud.ru/api/v1/auth/token"  # опционально
    )

Параметры
~~~~~~~~~

+-----------+-------+-----------------------------------------------+
| Параметр  | Тип   | Описание                                      |
+===========+=======+===============================================+
| ``key_id``| str   | ID ключа для аутентификации                   |
+-----------+-------+-----------------------------------------------+
| ``secret``| str   | Секретный ключ                                |
+-----------+-------+-----------------------------------------------+
| ``auth_url`` | str| URL сервера аутентификации (опционально)      |
+-----------+-------+-----------------------------------------------+

Основные методы
~~~~~~~~~~~~~~~

get_token()
~~~~~~~~~~~

Получает действительный токен доступа. Автоматически обновляет токен при необходимости.

.. code-block:: python

    def get_token(self) -> str:
        """
        Получить действительный токен доступа.
        
        Автоматически обновляет токен, если он истёк или истечёт в ближайшие 30 секунд.
        
        Returns:
            str: Действительный access_token
            
        Raises:
            RuntimeError: При ошибке получения токена
        """

**Пример:**
.. code-block:: python

    manager = TokenManager("key_id", "secret")
    token = manager.get_token()
    print(f"Токен: {token[:20]}...")

_refresh_token()
~~~~~~~~~~~~~~~~

Внутренний метод для обновления токена. Обычно вызывается автоматически.

.. code-block:: python

    def _refresh_token(self) -> str:
        """
        Обновить токен доступа.
        
        Выполняет HTTP запрос к серверу аутентификации для получения нового токена.
        
        Returns:
            str: Новый access_token
            
        Raises:
            RuntimeError: При ошибке HTTP запроса или неверном ответе
        """

Внутренняя логика
-----------------

Жизненный цикл токена
~~~~~~~~~~~~~~~~~~~~~

1. **Первый запрос**: При первом вызове ``get_token()`` выполняется аутентификация
2. **Кэширование**: Токен сохраняется в памяти с временем истечения
3. **Проверка срока**: При каждом запросе проверяется актуальность токена
4. **Автообновление**: Токен обновляется за 30 секунд до истечения
5. **Thread-safety**: Блокировка предотвращает одновременные запросы на обновление

Буферизация времени
~~~~~~~~~~~~~~~~~~~

Токен считается истёкшим за 30 секунд до реального истечения:

.. code-block:: python

    REFRESH_BUFFER_SECONDS = 30

    def _is_token_expired(self) -> bool:
        current_time = time.time()
        return current_time >= (self._token_expires_at - self.REFRESH_BUFFER_SECONDS)

Это обеспечивает:
- Предотвращение ошибок из-за истёкших токенов
- Бесперебойную работу API
- Минимальную задержку при запросах

Thread-safety
~~~~~~~~~~~~~

Класс использует блокировку для предотвращения race conditions:

.. code-block:: python

    import threading

    class TokenManager:
        def __init__(self, ...):
            self._lock = threading.Lock()
            # ...
        
        def get_token(self) -> str:
            with self._lock:
                if self._is_token_expired():
                    self._refresh_token()
                return self._token

Обработка ошибок
----------------

RuntimeError
~~~~~~~~~~~~

Возникает при проблемах с аутентификацией:

.. code-block:: python

    try:
        token = manager.get_token()
    except RuntimeError as e:
        print(f"Ошибка аутентификации: {e}")
        # Возможные причины:
        # - Неверные key_id/secret
        # - Проблемы с сетью
        # - Недоступность сервера аутентификации

Типичные ошибки
~~~~~~~~~~~~~~~

+-------------------+-------------------+-----------------------------------------------+
| Ошибка            | Причина           | Решение                                       |
+===================+===================+===============================================+
| ``HTTP 401``      | Неверные учетные  | Проверить key_id и secret                     |
|                   | данные            |                                               |
+-------------------+-------------------+-----------------------------------------------+
| ``HTTP 403``      | Отсутствие прав   | Обратиться к администратору                   |
|                   | доступа           |                                               |
+-------------------+-------------------+-----------------------------------------------+
| ``Connection      | Проблемы с сетью  | Проверить подключение                         |
| timeout``         |                   |                                               |
+-------------------+-------------------+-----------------------------------------------+
| ``Invalid         | Неожиданный ответ | Проверить auth_url                            |
| response format`` | сервера           |                                               |
+-------------------+-------------------+-----------------------------------------------+

Мониторинг
----------

Логирование
~~~~~~~~~~~

Для отладки можно добавить логирование:

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    class DebuggingTokenManager(TokenManager):
        def get_token(self) -> str:
            logger.debug("Запрос токена")
            token = super().get_token()
            logger.debug(f"Получен токен: {token[:10]}...")
            return token
        
        def _refresh_token(self) -> str:
            logger.info("Обновление токена")
            try:
                token = super()._refresh_token()
                logger.info("Токен успешно обновлен")
                return token
            except Exception as e:
                logger.error(f"Ошибка обновления токена: {e}")
                raise

Метрики
~~~~~~~

Отслеживание использования токенов:

.. code-block:: python

    import time
    from dataclasses import dataclass
    from typing import List

    @dataclass
    class TokenMetrics:
        refresh_time: float
        token_lifetime: float
        success: bool
        error: str = None

    class MetricsTokenManager(TokenManager):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.metrics: List[TokenMetrics] = []
        
        def _refresh_token(self) -> str:
            start_time = time.time()
            try:
                token = super()._refresh_token()
                refresh_duration = time.time() - start_time
                
                # Оценка времени жизни токена (обычно 3 минуты = 180 секунд)
                token_lifetime = self._token_expires_at - start_time
                
                metric = TokenMetrics(
                    refresh_time=refresh_duration,
                    token_lifetime=token_lifetime,
                    success=True
                )
                self.metrics.append(metric)
                return token
                
            except Exception as e:
                refresh_duration = time.time() - start_time
                metric = TokenMetrics(
                    refresh_time=refresh_duration,
                    token_lifetime=0,
                    success=False,
                    error=str(e)
                )
                self.metrics.append(metric)
                raise
        
        def get_stats(self):
            if not self.metrics:
                return "Нет данных"
            
            successful = [m for m in self.metrics if m.success]
            failed = [m for m in self.metrics if not m.success]
            
            if successful:
                avg_refresh_time = sum(m.refresh_time for m in successful) / len(successful)
                avg_lifetime = sum(m.token_lifetime for m in successful) / len(successful)
            else:
                avg_refresh_time = 0
                avg_lifetime = 0
            
            return {
                "total_refreshes": len(self.metrics),
                "successful_refreshes": len(successful),
                "failed_refreshes": len(failed),
                "success_rate": len(successful) / len(self.metrics) * 100,
                "avg_refresh_time": avg_refresh_time,
                "avg_token_lifetime": avg_lifetime
            }

Кастомизация
------------

Изменение времени буферизации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class CustomTokenManager(TokenManager):
        REFRESH_BUFFER_SECONDS = 60  # Обновлять за минуту до истечения
        
        def _is_token_expired(self) -> bool:
            current_time = time.time()
            return current_time >= (self._token_expires_at - self.REFRESH_BUFFER_SECONDS)

Альтернативный сервер аутентификации
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    manager = TokenManager(
        key_id="your-key-id",
        secret="your-secret",
        auth_url="https://custom-auth-server.com/api/v2/token"
    )

Retry механизм
~~~~~~~~~~~~~~

.. code-block:: python

    import time
    import random

    class RetryTokenManager(TokenManager):
        def _refresh_token(self, max_retries=3) -> str:
            for attempt in range(max_retries):
                try:
                    return super()._refresh_token()
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    # Экспоненциальная задержка с jitter
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    print(f"Повтор попытки {attempt + 1} через {delay:.2f}с")

Безопасность
------------

Защита учетных данных
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from cryptography.fernet import Fernet

    class SecureTokenManager(TokenManager):
        def __init__(self, encrypted_key_id, encrypted_secret, encryption_key):
            # Расшифровка учетных данных
            f = Fernet(encryption_key)
            key_id = f.decrypt(encrypted_key_id).decode()
            secret = f.decrypt(encrypted_secret).decode()
            
            super().__init__(key_id, secret)
            
            # Очистка переменных из памяти
            del key_id, secret

Ротация ключей
~~~~~~~~~~~~~~

.. code-block:: python

    class RotatingTokenManager:
        def __init__(self, primary_manager, backup_manager):
            self.primary = primary_manager
            self.backup = backup_manager
            self.use_backup = False
        
        def get_token(self) -> str:
            try:
                if not self.use_backup:
                    return self.primary.get_token()
                else:
                    return self.backup.get_token()
            except RuntimeError:
                # Переключение на резервные учетные данные
                self.use_backup = not self.use_backup
                if not self.use_backup:
                    return self.primary.get_token()
                else:
                    return self.backup.get_token()

Интеграция
----------

Использование в EvolutionInference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TokenManager автоматически интегрирован в EvolutionInference:

.. code-block:: python

    # Внутри EvolutionInference
    class EvolutionInference(BaseLLM):
        def __init__(self, key_id, secret, ...):
            self._token_manager = TokenManager(key_id, secret)
        
        def _make_request(self, ...):
            token = self._token_manager.get_token()
            headers = {"Authorization": f"Bearer {token}"}
            # ... выполнение запроса

Независимое использование
~~~~~~~~~~~~~~~~~~~~~~~~~

Можно использовать TokenManager отдельно:

.. code-block:: python

    import requests

    manager = TokenManager("key_id", "secret")

    def make_api_request(data):
        token = manager.get_token()
        
        response = requests.post(
            "https://api.cloud-ru-tech.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}"},
            json=data
        )
        
        return response.json()

См. также
---------

* :doc:`evolution-inference` - Основной класс LLM
* :doc:`../guide/token-management` - Подробное руководство
* :doc:`../guide/error-handling` - Работа с ошибками 