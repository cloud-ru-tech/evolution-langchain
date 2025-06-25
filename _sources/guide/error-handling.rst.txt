Обработка ошибок
================

Этот раздел содержит подробное руководство по обработке ошибок в Evolution LangChain.

Типы ошибок
-----------

ValueError
~~~~~~~~~~

Возникает при неверной конфигурации или параметрах:

.. code-block:: python

   from evolution_langchain import EvolutionInference

   try:
       # Отсутствует обязательный параметр base_url
       llm = EvolutionInference(
           model="test-model",
           key_id="test-key",
           secret="test-secret"
           # base_url отсутствует
       )
   except ValueError as e:
       print(f"Ошибка конфигурации: {e}")
       # Ошибка: base_url is required

Типичные случаи ValueError:
- Отсутствие обязательных параметров
- Неверный формат URL
- Некорректные значения параметров генерации

RuntimeError
~~~~~~~~~~~~

Возникает при проблемах с API запросами:

.. code-block:: python

   try:
       llm = EvolutionInference(
           model="test-model",
           key_id="invalid-key",
           secret="invalid-secret",
           base_url="https://invalid-url.com/v1"
       )
       
       response = llm.invoke("Тест")
   except RuntimeError as e:
       print(f"Ошибка API: {e}")
       # Возможные причины:
       # - Неверные учетные данные
       # - Недоступность сервиса
       # - Проблемы с сетью

Обработка ошибок аутентификации
-------------------------------

Неверные учетные данные
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from evolution_langchain import EvolutionInference

   def create_llm_with_retry(max_retries=3):
       """Создание LLM с повтором при ошибках аутентификации."""
       
       credentials = [
           ("primary-key", "primary-secret"),
           ("backup-key", "backup-secret"),
           ("fallback-key", "fallback-secret")
       ]
       
       for attempt in range(max_retries):
           try:
               key_id, secret = credentials[attempt % len(credentials)]
               
               llm = EvolutionInference(
                   model="your-model",
                   key_id=key_id,
                   secret=secret,
                   base_url="https://your-api-endpoint.com/v1"
               )
               
               # Тестовый запрос для проверки
               llm.invoke("test")
               return llm
               
           except RuntimeError as e:
               print(f"Попытка {attempt + 1} неудачна: {e}")
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Экспоненциальная задержка
               else:
                   raise Exception("Все попытки аутентификации исчерпаны")

   # Использование
   try:
       llm = create_llm_with_retry()
       print("✅ LLM успешно создан")
   except Exception as e:
       print(f"❌ Не удалось создать LLM: {e}")

Истечение токена
~~~~~~~~~~~~~~~~

.. code-block:: python

   def safe_invoke(llm, prompt, max_retries=3):
       """Безопасный вызов с обработкой истечения токена."""
       
       for attempt in range(max_retries):
           try:
               return llm.invoke(prompt)
               
           except RuntimeError as e:
               error_msg = str(e).lower()
               
               if "token" in error_msg or "401" in error_msg or "403" in error_msg:
                   print(f"Ошибка токена на попытке {attempt + 1}: {e}")
                   
                   if attempt < max_retries - 1:
                       # Принудительно сбросить токен
                       if hasattr(llm, '_token_manager'):
                           llm._token_manager._token = None
                           llm._token_manager._token_expires_at = 0
                       
                       time.sleep(1)  # Небольшая задержка
                       continue
                
               # Не связано с токеном - прокинуть ошибку
               raise
       
       raise RuntimeError(f"Превышено количество попыток: {max_retries}")

   # Использование
   try:
       response = safe_invoke(llm, "Привет!")
       print(response)
   except RuntimeError as e:
       print(f"Ошибка запроса: {e}")

Обработка сетевых ошибок
------------------------

Таймауты и недоступность сервиса
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from requests.exceptions import RequestException, Timeout, ConnectionError

   class RobustEvolutionInference:
       def __init__(self, **kwargs):
           self.config = kwargs
           self.llm = None
           self._initialize_llm()
       
       def _initialize_llm(self):
           """Инициализация LLM с проверкой доступности."""
           try:
               # Проверить доступность API endpoint
               base_url = self.config['base_url']
               test_url = base_url.replace('/v1', '/health')  # Endpoint для проверки здоровья
               
               response = requests.get(test_url, timeout=5)
               if response.status_code != 200:
                   print(f"⚠️  API endpoint может быть недоступен: {response.status_code}")
                
           except (ConnectionError, Timeout) as e:
               print(f"⚠️  Проблемы с подключением к API: {e}")
           except Exception as e:
               print(f"⚠️  Неизвестная ошибка при проверке API: {e}")
            
           # Создать LLM несмотря на предупреждения
           self.llm = EvolutionInference(**self.config)
       
       def invoke(self, prompt, timeout=30):
           """Вызов с расширенной обработкой ошибок."""
           try:
               # Установить таймаут через конфигурацию
               old_timeout = self.llm.request_timeout
               self.llm.request_timeout = timeout
               
               response = self.llm.invoke(prompt)
               
               # Восстановить таймаут
               self.llm.request_timeout = old_timeout
               
               return response
               
           except RuntimeError as e:
               error_msg = str(e).lower()
               
               if "timeout" in error_msg:
                   raise TimeoutError(f"Запрос превысил таймаут {timeout}с")
               elif "connection" in error_msg:
                   raise ConnectionError("Проблемы с сетевым подключением")
               else:
                   raise e

   # Использование
   robust_llm = RobustEvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   try:
       response = robust_llm.invoke("Привет!", timeout=10)
       print(response)
   except TimeoutError as e:
       print(f"Таймаут: {e}")
   except ConnectionError as e:
       print(f"Ошибка подключения: {e}")

Обработка ошибок генерации
--------------------------

Ограничения токенов
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def handle_token_limit_error(llm, prompt, max_tokens=512):
       """Обработка ошибок превышения лимита токенов."""
       
       try:
           # Попытка с исходными параметрами
           response = llm.invoke(prompt)
           return response
           
       except RuntimeError as e:
           error_msg = str(e).lower()
           
           if "token" in error_msg and ("limit" in error_msg or "length" in error_msg):
               print("⚠️  Превышен лимит токенов, уменьшаю промпт...")
               
               # Уменьшить промпт
               shortened_prompt = prompt[:len(prompt)//2] + "..."
               
               # Попробовать с уменьшенным промптом
               try:
                   response = llm.invoke(shortened_prompt)
                   return response + "\n\n[Ответ сокращен из-за ограничений]"
               except RuntimeError as e2:
                   print(f"❌ Не удалось обработать даже сокращенный промпт: {e2}")
                   raise e2
           else:
               raise e

   # Использование
   long_prompt = "Очень длинный промпт..." * 1000  # Искусственно длинный
   
   try:
       response = handle_token_limit_error(llm, long_prompt)
       print(response)
   except RuntimeError as e:
       print(f"Ошибка: {e}")

Обработка ошибок параметров
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def validate_and_fix_parameters(llm, **kwargs):
       """Валидация и исправление параметров генерации."""
       
       # Проверка и исправление temperature
       if 'temperature' in kwargs:
           temp = kwargs['temperature']
           if temp < 0:
               print(f"⚠️  Temperature {temp} слишком низкий, устанавливаю 0")
               kwargs['temperature'] = 0
           elif temp > 2:
               print(f"⚠️  Temperature {temp} слишком высокий, устанавливаю 2")
               kwargs['temperature'] = 2
       
       # Проверка и исправление max_tokens
       if 'max_tokens' in kwargs:
           max_tokens = kwargs['max_tokens']
           if max_tokens < 1:
               print(f"⚠️  Max tokens {max_tokens} слишком низкий, устанавливаю 1")
               kwargs['max_tokens'] = 1
           elif max_tokens > 4000:
               print(f"⚠️  Max tokens {max_tokens} слишком высокий, устанавливаю 4000")
               kwargs['max_tokens'] = 4000
       
       return kwargs

   # Использование
   try:
       # Попытка с некорректными параметрами
       response = llm.invoke("Привет!", temperature=5.0, max_tokens=10000)
   except RuntimeError as e:
       print(f"Ошибка с некорректными параметрами: {e}")
       
       # Исправление параметров
       fixed_params = validate_and_fix_parameters(llm, temperature=5.0, max_tokens=10000)
       response = llm.invoke("Привет!", **fixed_params)
       print(f"Исправленный ответ: {response}")

Логирование ошибок
------------------

Настройка логирования
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import time
   from datetime import datetime

   # Настройка логирования
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('evolution_errors.log'),
           logging.StreamHandler()
       ]
   )

   logger = logging.getLogger(__name__)

   class LoggedEvolutionInference:
       def __init__(self, llm):
           self.llm = llm
           self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
       
       def invoke(self, prompt):
           start_time = time.time()
           
           try:
               self.logger.info(f"Начало запроса: {prompt[:50]}...")
               response = self.llm.invoke(prompt)
               
               duration = time.time() - start_time
               self.logger.info(f"Запрос выполнен за {duration:.2f}с")
               
               return response
               
           except Exception as e:
               duration = time.time() - start_time
               self.logger.error(
                   f"Ошибка запроса за {duration:.2f}с: {type(e).__name__}: {e}"
               )
               raise

   # Использование
   logged_llm = LoggedEvolutionInference(llm)

   try:
       response = logged_llm.invoke("Привет!")
       print(response)
   except Exception as e:
       print(f"Ошибка: {e}")

Метрики ошибок
~~~~~~~~~~~~~~

.. code-block:: python

   from dataclasses import dataclass
   from typing import Dict, List
   import time

   @dataclass
   class ErrorMetric:
       error_type: str
       count: int = 0
       last_occurrence: str = ""
       avg_response_time: float = 0.0

   class ErrorTrackingEvolutionInference:
       def __init__(self, llm):
           self.llm = llm
           self.error_metrics: Dict[str, ErrorMetric] = {}
           self.total_requests = 0
           self.successful_requests = 0
       
       def invoke(self, prompt):
           start_time = time.time()
           self.total_requests += 1
           
           try:
               response = self.llm.invoke(prompt)
               self.successful_requests += 1
               return response
               
           except Exception as e:
               error_type = type(e).__name__
               duration = time.time() - start_time
               
               # Обновление метрик ошибок
               if error_type not in self.error_metrics:
                   self.error_metrics[error_type] = ErrorMetric(error_type)
               
               metric = self.error_metrics[error_type]
               metric.count += 1
               metric.last_occurrence = datetime.now().isoformat()
               
               # Обновление среднего времени
               if metric.count == 1:
                   metric.avg_response_time = duration
               else:
                   metric.avg_response_time = (
                       (metric.avg_response_time * (metric.count - 1) + duration) 
                       / metric.count
                   )
               
               raise e
       
       def get_error_report(self):
           """Получение отчета об ошибках."""
           success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
           
           return {
               "total_requests": self.total_requests,
               "successful_requests": self.successful_requests,
               "success_rate": success_rate,
               "error_metrics": self.error_metrics
           }

   # Использование
   tracked_llm = ErrorTrackingEvolutionInference(llm)

   # Выполнение запросов
   for i in range(5):
       try:
           response = tracked_llm.invoke(f"Запрос {i}")
           print(f"✅ Запрос {i} успешен")
       except Exception as e:
           print(f"❌ Запрос {i} неудачен: {e}")

   # Получение отчета
   report = tracked_llm.get_error_report()
   print(f"Отчет: {report}")

Полный пример обработки ошибок
------------------------------

Объединение всех методов обработки ошибок:

.. code-block:: python

   import os
   import time
   import logging
   from dataclasses import dataclass
   from typing import Optional, Dict, Any
   from evolution_langchain import EvolutionInference

   @dataclass
   class ErrorConfig:
       max_retries: int = 3
       retry_delay: float = 1.0
       timeout: int = 30
       enable_logging: bool = True
       enable_metrics: bool = True

   class ComprehensiveErrorHandler:
       def __init__(self, llm, config: ErrorConfig):
           self.llm = llm
           self.config = config
           self.metrics = {
               "total_requests": 0,
               "successful_requests": 0,
               "errors": {}
           }
           
           if config.enable_logging:
               logging.basicConfig(level=logging.INFO)
               self.logger = logging.getLogger(__name__)
           else:
               self.logger = None
       
       def invoke(self, prompt: str, **kwargs) -> str:
           """Вызов с полной обработкой ошибок."""
           self.metrics["total_requests"] += 1
           
           for attempt in range(self.config.max_retries):
               start_time = time.time()
               
               try:
                   # Логирование начала запроса
                   if self.logger:
                       self.logger.info(f"Запрос {attempt + 1}: {prompt[:50]}...")
                   
                   # Выполнение запроса
                   response = self.llm.invoke(prompt, **kwargs)
                   
                   # Успешное выполнение
                   duration = time.time() - start_time
                   self.metrics["successful_requests"] += 1
                   
                   if self.logger:
                       self.logger.info(f"Запрос выполнен за {duration:.2f}с")
                   
                   return response
                   
               except ValueError as e:
                   # Ошибки конфигурации - не повторяем
                   self._record_error("ValueError", e, duration=time.time() - start_time)
                   raise e
                   
               except RuntimeError as e:
                   duration = time.time() - start_time
                   error_msg = str(e).lower()
                   
                   # Определение типа ошибки
                   if "authentication" in error_msg or "401" in error_msg or "403" in error_msg:
                       error_type = "AuthenticationError"
                   elif "timeout" in error_msg:
                       error_type = "TimeoutError"
                   elif "connection" in error_msg:
                       error_type = "ConnectionError"
                   elif "token" in error_msg and "limit" in error_msg:
                       error_type = "TokenLimitError"
                   else:
                       error_type = "RuntimeError"
                   
                   self._record_error(error_type, e, duration)
                   
                   # Логирование ошибки
                   if self.logger:
                       self.logger.warning(
                           f"Попытка {attempt + 1} неудачна: {error_type}: {e}"
                       )
                   
                   # Решение в зависимости от типа ошибки
                   if error_type == "TokenLimitError":
                       # Сокращение промпта
                       shortened_prompt = prompt[:len(prompt)//2] + "..."
                       if self.logger:
                           self.logger.info("Сокращаю промпт из-за лимита токенов")
                       prompt = shortened_prompt
                       continue
                   
                   elif error_type == "AuthenticationError":
                       # Сброс токена
                       if hasattr(self.llm, '_token_manager'):
                           self.llm._token_manager._token = None
                           self.llm._token_manager._token_expires_at = 0
                       if self.logger:
                           self.logger.info("Сбрасываю токен аутентификации")
                   
                   # Повторная попытка
                   if attempt < self.config.max_retries - 1:
                       delay = self.config.retry_delay * (2 ** attempt)
                       if self.logger:
                           self.logger.info(f"Ожидание {delay}с перед повторной попыткой")
                       time.sleep(delay)
                       continue
                   
                   # Все попытки исчерпаны
                   if self.logger:
                       self.logger.error(f"Все попытки исчерпаны: {e}")
                   raise e
                   
               except Exception as e:
                   # Неожиданные ошибки
                   duration = time.time() - start_time
                   self._record_error("UnexpectedError", e, duration)
                   
                   if self.logger:
                       self.logger.error(f"Неожиданная ошибка: {type(e).__name__}: {e}")
                   raise e
           
           raise RuntimeError("Все попытки исчерпаны")
       
       def _record_error(self, error_type: str, error: Exception, duration: float):
           """Запись метрик ошибки."""
           if not self.config.enable_metrics:
               return
           
           if error_type not in self.metrics["errors"]:
               self.metrics["errors"][error_type] = {
                   "count": 0,
                   "last_occurrence": "",
                   "avg_duration": 0.0
               }
           
           error_metric = self.metrics["errors"][error_type]
           error_metric["count"] += 1
           error_metric["last_occurrence"] = time.strftime("%Y-%m-%d %H:%M:%S")
           
           # Обновление среднего времени
           if error_metric["count"] == 1:
               error_metric["avg_duration"] = duration
           else:
               error_metric["avg_duration"] = (
                   (error_metric["avg_duration"] * (error_metric["count"] - 1) + duration) 
                   / error_metric["count"]
               )
       
       def get_metrics(self) -> Dict[str, Any]:
           """Получение метрик."""
           if not self.config.enable_metrics:
               return {}
           
           success_rate = (
               (self.metrics["successful_requests"] / self.metrics["total_requests"] * 100) 
               if self.metrics["total_requests"] > 0 else 0
           )
           
           return {
               "total_requests": self.metrics["total_requests"],
               "successful_requests": self.metrics["successful_requests"],
               "success_rate": success_rate,
               "errors": self.metrics["errors"]
           }

   def main():
       print("🚀 Evolution LangChain - Обработка ошибок")
       print("=" * 50)

       # Создание LLM
       llm = EvolutionInference(
           model=os.getenv("EVOLUTION_MODEL", "your-model"),
           key_id=os.getenv("EVOLUTION_KEY_ID", "your-key-id"),
           secret=os.getenv("EVOLUTION_SECRET", "your-secret"),
           base_url=os.getenv("EVOLUTION_BASE_URL", "https://your-api-endpoint.com/v1")
       )

       # Создание обработчика ошибок
       config = ErrorConfig(
           max_retries=3,
           retry_delay=1.0,
           timeout=30,
           enable_logging=True,
           enable_metrics=True
       )

       error_handler = ComprehensiveErrorHandler(llm, config)

       print("✅ Обработчик ошибок инициализирован")
       print()

       # Тестирование различных сценариев
       test_cases = [
           "Привет! Как дела?",
           "Расскажи о машинном обучении",
           "Очень длинный промпт..." * 1000,  # Тест лимита токенов
           "Тест с некорректными параметрами"
       ]

       for i, test_case in enumerate(test_cases, 1):
           print(f"Тест {i}: {test_case[:50]}...")
           
           try:
               if i == 4:  # Тест с некорректными параметрами
                   response = error_handler.invoke(test_case, temperature=5.0)
               else:
                   response = error_handler.invoke(test_case)
               
               print(f"✅ Успех: {response[:100]}...")
               
           except Exception as e:
               print(f"❌ Ошибка: {type(e).__name__}: {e}")
           
           print()

       # Вывод метрик
       metrics = error_handler.get_metrics()
       print("📊 Метрики:")
       for key, value in metrics.items():
           if key == "errors":
               print(f"  {key}:")
               for error_type, error_data in value.items():
                   print(f"    {error_type}: {error_data}")
           else:
               print(f"  {key}: {value}")

   if __name__ == "__main__":
       main()

Что дальше?
-----------

- Изучите :doc:`../guide/token-management` для понимания управления токенами
- Прочитайте :doc:`../guide/langchain-integration` для интеграции с LangChain
- Посмотрите :doc:`../api/evolution-inference` для полной документации API 