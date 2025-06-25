Основы использования
====================

Этот раздел содержит подробное руководство по использованию Evolution LangChain.

Инициализация
-------------

Базовая инициализация
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference

   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

Полная инициализация с параметрами
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   llm = EvolutionInference(
       # Обязательные параметры
       model="your-model-name",
       key_id="your-key-id", 
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       
       # Настройки аутентификации
       auth_url="https://iam.api.cloud.ru/api/v1/auth/token",
       
       # Параметры генерации
       temperature=0.7,
       max_tokens=1000,
       top_p=1.0,
       frequency_penalty=0.0,
       presence_penalty=0.0,
       stop=None,
       
       # Настройки сети
       request_timeout=60,
   )

Параметры конфигурации
----------------------

Обязательные параметры
~~~~~~~~~~~~~~~~~~~~~~

+------------+------+------------------------------------------+
| Параметр   | Тип  | Описание                                 |
+============+======+==========================================+
| ``model``  | str  | Название модели для использования        |
+------------+------+------------------------------------------+
| ``key_id`` | str  | ID ключа для аутентификации              |
+------------+------+------------------------------------------+
| ``secret`` | str  | Секретный ключ для аутентификации        |
+------------+------+------------------------------------------+
| ``base_url`` | str | Базовый URL API Evolution Inference     |
+------------+------+------------------------------------------+

Опциональные параметры
~~~~~~~~~~~~~~~~~~~~~~

+-------------------+--------+------------------+------------------------------------------+
| Параметр          | Тип    | По умолчанию     | Описание                                 |
+===================+========+==================+==========================================+
| ``auth_url``      | str    | предустановлен   | URL сервера аутентификации               |
+-------------------+--------+------------------+------------------------------------------+
| ``temperature``   | float  | ``1.0``          | Контроль случайности генерации           |
+-------------------+--------+------------------+------------------------------------------+
| ``max_tokens``    | int    | ``512``          | Максимальное количество токенов          |
+-------------------+--------+------------------+------------------------------------------+
| ``top_p``         | float  | ``1.0``          | Nucleus sampling                         |
+-------------------+--------+------------------+------------------------------------------+
| ``frequency_penalty`` | float | ``0.0``    | Штраф за частоту повторений                 |
+-------------------+--------+------------------+------------------------------------------+
| ``presence_penalty`` | float | ``0.0``     | Штраф за присутствие токенов                |
+-------------------+--------+------------------+------------------------------------------+
| ``stop``          | List[str] | ``None``   | Последовательности остановки                |
+-------------------+--------+------------------+------------------------------------------+
| ``request_timeout`` | int   | ``60``          | Таймаут запросов (секунды)               |
+-------------------+--------+------------------+------------------------------------------+

Основные методы
---------------

invoke() - Одиночный запрос
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Самый простой способ отправить запрос:

.. code-block:: python

   response = llm.invoke("Расскажи о машинном обучении")
   print(response)

generate() - Пакетная обработка
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Для обработки нескольких промптов одновременно:

.. code-block:: python

   prompts = [
       "Что такое Python?",
       "Что такое JavaScript?",
       "Что такое машинное обучение?"
   ]

   responses = llm.generate(prompts)

   for i, generation_list in enumerate(responses.generations):
       print(f"Промпт {i+1}: {prompts[i]}")
       print(f"Ответ: {generation_list[0].text}")
       print("-" * 50)

Асинхронные методы
~~~~~~~~~~~~~~~~~~

Для асинхронного выполнения запросов:

.. code-block:: python

   import asyncio

   async def async_example():
       # Асинхронный одиночный запрос
       response = await llm.ainvoke("Расскажи о квантовых компьютерах")
       print(response)
       
       # Асинхронная пакетная обработка
       prompts = ["Вопрос 1", "Вопрос 2", "Вопрос 3"]
       responses = await llm.agenerate(prompts)
       
       return responses

   # Запуск асинхронной функции
   asyncio.run(async_example())

Настройка параметров генерации
------------------------------

Temperature (Температура)
~~~~~~~~~~~~~~~~~~~~~~~~~

Контролирует случайность в генерации текста:

.. code-block:: python

   # Более детерминированные ответы
   llm_conservative = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       temperature=0.1  # Низкая случайность
   )

   # Более креативные ответы
   llm_creative = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       temperature=1.5  # Высокая случайность
   )

Max Tokens (Максимальное количество токенов)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ограничивает длину ответа:

.. code-block:: python

   # Короткие ответы
   llm_short = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret", 
       base_url="https://your-api-endpoint.com/v1",
       max_tokens=50
   )

   # Длинные ответы
   llm_long = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       max_tokens=2000
   )

Stop Sequences (Последовательности остановки)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Определяют, где остановить генерацию:

.. code-block:: python

   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       stop=["\n\n", "Конец", "###"]
   )

Top-p (Nucleus Sampling)
~~~~~~~~~~~~~~~~~~~~~~~~

Контролирует разнообразие через nucleus sampling:

.. code-block:: python

   # Более разнообразные ответы
   llm_diverse = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       top_p=0.8
   )

   # Более предсказуемые ответы
   llm_focused = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       top_p=0.95
   )

Штрафы
~~~~~~

Frequency Penalty и Presence Penalty:

.. code-block:: python

   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       frequency_penalty=0.5,  # Штраф за повторения
       presence_penalty=0.3    # Штраф за присутствие токенов
   )

Интеграция с LangChain
----------------------

Создание цепочек
~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate

   # Создание шаблона
   template = """
   Ты - эксперт по {topic}. Ответь на вопрос подробно и информативно.
   
   Вопрос: {question}
   
   Ответ:"""

   prompt = PromptTemplate(
       template=template,
       input_variables=["topic", "question"]
   )

   # Создание LLM
   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание цепочки
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение
   result = chain.run({
       "topic": "машинное обучение",
       "question": "Что такое нейронные сети?"
   })

Использование с агентами
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.agents import initialize_agent, Tool
   from langchain.tools import DuckDuckGoSearchRun

   # Создание инструментов
   search = DuckDuckGoSearchRun()
   tools = [
       Tool(
           name="Search",
           func=search.run,
           description="Полезно для поиска актуальной информации"
       )
   ]

   # Создание LLM
   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание агента
   agent = initialize_agent(
       tools, llm, agent="zero-shot-react-description", verbose=True
   )

   # Выполнение
   agent.run("Какая погода в Москве сегодня?")

Работа с векторными хранилищами
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.embeddings import OpenAIEmbeddings
   from langchain.vectorstores import Chroma
   from langchain.text_splitter import CharacterTextSplitter

   # Создание LLM
   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание векторного хранилища
   embeddings = OpenAIEmbeddings()
   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   texts = text_splitter.split_text("Ваш текст здесь...")
   vectorstore = Chroma.from_texts(texts, embeddings)

   # Поиск и ответ
   docs = vectorstore.similarity_search("Ваш вопрос")
   context = "\n".join([doc.page_content for doc in docs])
   
   response = llm.invoke(f"Контекст: {context}\n\nВопрос: Ваш вопрос")
   print(response)

Обработка ошибок
----------------

Базовая обработка ошибок
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference

   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   try:
       response = llm.invoke("Привет!")
       print(response)
   except Exception as e:
       print(f"Произошла ошибка: {e}")
       print(f"Тип ошибки: {type(e).__name__}")

Продвинутая обработка ошибок
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from evolution_langchain import EvolutionInference

   def make_request_with_retry(llm, prompt, max_retries=3):
       for attempt in range(max_retries):
           try:
               response = llm.invoke(prompt)
               return response
           except Exception as e:
               print(f"Попытка {attempt + 1} не удалась: {e}")
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Экспоненциальная задержка
               else:
                   raise e

   llm = EvolutionInference(
       model="your-model",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   try:
       response = make_request_with_retry(llm, "Расскажи анекдот")
       print(response)
   except Exception as e:
       print(f"Все попытки не удались: {e}")

Что дальше?
-----------

- Изучите :doc:`langchain-integration` для продвинутых паттернов интеграции
- Прочитайте :doc:`token-management` для понимания управления токенами
- Посмотрите :doc:`error-handling` для детальной обработки ошибок
- Изучите :doc:`../examples/advanced` для сложных примеров использования 