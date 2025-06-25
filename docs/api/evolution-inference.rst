EvolutionInference
==================

.. automodule:: evolution_langchain.evolution_inference
   :members:
   :undoc-members:
   :show-inheritance:

Обзор
-----

``EvolutionInference`` - это основной класс для работы с Evolution Inference API через LangChain. Он наследуется от ``BaseLLM`` и предоставляет полную совместимость с экосистемой LangChain.

Быстрый пример
--------------

.. code-block:: python

    from evolution_langchain import EvolutionInference

    # Создание экземпляра
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret", 
        base_url="https://your-api-endpoint.com/v1"
    )

    # Простой запрос
    response = llm.invoke("Привет!")
    print(response)

Параметры инициализации
-----------------------

Обязательные параметры
~~~~~~~~~~~~~~~~~~~~~~~

+-----------+-------+-----------------------------------------------+
| Параметр  | Тип   | Описание                                      |
+===========+=======+===============================================+
| ``model`` | str   | Название модели для использования             |
+-----------+-------+-----------------------------------------------+
| ``key_id``| str   | ID ключа для аутентификации                   |
+-----------+-------+-----------------------------------------------+
| ``secret``| str   | Секретный ключ для аутентификации             |
+-----------+-------+-----------------------------------------------+
| ``base_url`` | str| Базовый URL API Evolution Inference           |
+-----------+-------+-----------------------------------------------+

Опциональные параметры
~~~~~~~~~~~~~~~~~~~~~~~

+---------------------+----------+-------------------+-----------------------------------------------+
| Параметр            | Тип      | По умолчанию      | Описание                                      |
+=====================+==========+===================+===============================================+
| ``auth_url``        | str      | предустановлен    | URL сервера аутентификации                    |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``temperature``     | float    | ``1.0``           | Контроль случайности генерации                |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``max_tokens``      | int      | ``512``           | Максимальное количество токенов               |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``top_p``           | float    | ``1.0``           | Nucleus sampling                              |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``frequency_penalty`` | float  | ``0.0``           | Штраф за частоту повторений                   |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``presence_penalty``  | float  | ``0.0``           | Штраф за присутствие токенов                  |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``stop``            | List[str]| ``None``          | Последовательности остановки                  |
+---------------------+----------+-------------------+-----------------------------------------------+
| ``request_timeout`` | int      | ``60``            | Таймаут запросов (секунды)                    |
+---------------------+----------+-------------------+-----------------------------------------------+

Основные методы
~~~~~~~~~~~~~~~

invoke()
~~~~~~~~

Выполняет одиночный запрос к модели.

.. code-block:: python

    def invoke(self, input: str, config: Optional[RunnableConfig] = None) -> str:
        """
        Выполнить запрос к модели.
        
        Args:
            input: Входной текст промпта
            config: Конфигурация выполнения (опционально)
            
        Returns:
            str: Ответ модели
            
        Raises:
            RuntimeError: При ошибке API запроса
            ValueError: При неверных параметрах
        """

**Пример:**
.. code-block:: python

    response = llm.invoke("Что такое машинное обучение?")
    print(response)

generate()
~~~~~~~~~~

Выполняет пакетную обработку нескольких промптов.

.. code-block:: python

    def generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        """
        Выполнить пакетную генерацию для списка промптов.
        
        Args:
            prompts: Список входных промптов
            stop: Последовательности остановки (переопределяет значение по умолчанию)
            
        Returns:
            LLMResult: Результат с поколениями для каждого промпта
            
        Raises:
            RuntimeError: При ошибке API запроса
        """

**Пример:**
.. code-block:: python

    prompts = ["Вопрос 1", "Вопрос 2", "Вопрос 3"]
    responses = llm.generate(prompts)

    for i, generation_list in enumerate(responses.generations):
        print(f"Промпт {i+1}: {prompts[i]}")
        print(f"Ответ: {generation_list[0].text}")

ainvoke()
~~~~~~~~~

Асинхронная версия ``invoke()``.

.. code-block:: python

    async def ainvoke(self, input: str, config: Optional[RunnableConfig] = None) -> str:
        """
        Асинхронно выполнить запрос к модели.
        
        Args:
            input: Входной текст промпта
            config: Конфигурация выполнения (опционально)
            
        Returns:
            str: Ответ модели
        """

**Пример:**
.. code-block:: python

    import asyncio

    async def main():
        response = await llm.ainvoke("Асинхронный вопрос")
        print(response)

    asyncio.run(main())

agenerate()
~~~~~~~~~~~

Асинхронная версия ``generate()``.

.. code-block:: python

    async def agenerate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        """
        Асинхронно выполнить пакетную генерацию.
        
        Args:
            prompts: Список входных промптов
            stop: Последовательности остановки
            
        Returns:
            LLMResult: Результат генерации
        """

Свойства
--------

_llm_type
~~~~~~~~~

Возвращает тип LLM для идентификации.

.. code-block:: python

    @property
    def _llm_type(self) -> str:
        """Тип LLM."""
        return "cloud-ru-tech"

_default_params
~~~~~~~~~~~~~~~

Возвращает параметры по умолчанию для запросов.

.. code-block:: python

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Параметры по умолчанию для API запросов."""

Управление токенами
-------------------

Класс автоматически управляет жизненным циклом токенов доступа через внутренний ``TokenManager``:

- ✅ Автоматическое получение токена при первом запросе
- ✅ Кэширование токена в памяти
- ✅ Автоматическое обновление за 30 секунд до истечения
- ✅ Thread-safe операции
- ✅ Обработка ошибок аутентификации

Обработка ошибок
----------------

ValueError
~~~~~~~~~~

Возникает при неверных параметрах конфигурации:

.. code-block:: python

    try:
        llm = EvolutionInference(
            model="test",
            # Отсутствуют key_id и secret
            base_url="https://test.com/v1"
        )
    except ValueError as e:
        print(f"Ошибка конфигурации: {e}")

RuntimeError
~~~~~~~~~~~~

Возникает при ошибках API запросов:

.. code-block:: python

    try:
        response = llm.invoke("Тестовый запрос")
    except RuntimeError as e:
        print(f"Ошибка API: {e}")

Интеграция с LangChain
----------------------

Использование в цепочках
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate

    template = "Ответь на вопрос: {question}"
    prompt = PromptTemplate(template=template, input_variables=["question"])

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run("Что такое искусственный интеллект?")

Использование с агентами
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.agents import initialize_agent, Tool
    from langchain.agents import AgentType

    # Создание инструментов
    tools = [
        Tool(
            name="search",
            func=lambda x: f"Результат поиска для: {x}",
            description="Поиск информации"
        )
    ]

    # Создание агента
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Выполнение задачи
    result = agent.run("Найди информацию о Python")

Примеры конфигурации
--------------------

Консервативная конфигурация (детерминированные ответы)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    llm_conservative = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        temperature=0.1,
        max_tokens=200,
        top_p=0.8,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

Креативная конфигурация (разнообразные ответы)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    llm_creative = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        temperature=1.2,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

Конфигурация для диалогов
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    llm_chat = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        temperature=0.7,
        max_tokens=300,
        stop=["Human:", "AI:", "\n\n"]
    )

Лучшие практики
---------------

1. Использование переменных окружения
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os

    llm = EvolutionInference(
        model=os.getenv("EVOLUTION_MODEL"),
        key_id=os.getenv("EVOLUTION_KEY_ID"),
        secret=os.getenv("EVOLUTION_SECRET"),
        base_url=os.getenv("EVOLUTION_BASE_URL")
    )

2. Обработка ошибок
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def safe_invoke(llm, prompt, max_retries=3):
        for attempt in range(max_retries):
            try:
                return llm.invoke(prompt)
            except RuntimeError as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Попытка {attempt + 1} неудачна: {e}")
                time.sleep(2 ** attempt)  # Экспоненциальная задержка

3. Мониторинг использования
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time

    class MonitoredEvolutionInference:
        def __init__(self, llm):
            self.llm = llm
            self.request_count = 0
            self.total_time = 0
        
        def invoke(self, prompt):
            start = time.time()
            try:
                response = self.llm.invoke(prompt)
                self.request_count += 1
                self.total_time += time.time() - start
                return response
            except Exception as e:
                print(f"Ошибка после {self.request_count} запросов: {e}")
                raise
        
        def get_stats(self):
            if self.request_count == 0:
                return "Запросов не было"
            
            avg_time = self.total_time / self.request_count
            return f"Запросов: {self.request_count}, Среднее время: {avg_time:.2f}с"

См. также
---------

* :doc:`token-manager` - Управление токенами аутентификации
* :doc:`../guide/basics` - Подробное руководство
* :doc:`../examples/basic` - Практические примеры использования 