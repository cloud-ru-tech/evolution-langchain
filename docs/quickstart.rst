Быстрый старт
=============

Этот раздел поможет вам быстро начать работу с Evolution LangChain.

Установка
---------

Установите SDK через pip:

.. code-block:: bash

   pip install evolution-langchain

Или, если вы используете Poetry:

.. code-block:: bash

   poetry add evolution-langchain

Получение учетных данных
------------------------

Для работы с Evolution LangChain вам понадобятся:

1. **Key ID** - идентификатор ключа доступа
2. **Secret** - секретный ключ
3. **Base URL** - URL эндпоинта вашей модели
4. **Model name** - название модели для использования

Эти данные можно получить в личном кабинете Cloud.ru.

Первый запрос
-------------

Создайте файл ``example.py`` и добавьте следующий код:

.. code-block:: python

   from evolution_langchain import EvolutionInference

   # Инициализация модели
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your_key_id",
       secret="your_secret",
       base_url="https://your-endpoint.cloud.ru/v1"
   )

   # Выполнение запроса
   response = llm.invoke("Привет! Расскажи анекдот.")
   print(response)

Запустите скрипт:

.. code-block:: bash

   python example.py

Использование переменных окружения
----------------------------------

Для безопасности рекомендуется использовать переменные окружения:

.. code-block:: bash

   export EVOLUTION_KEY_ID="your_key_id"
   export EVOLUTION_SECRET="your_secret"
   export EVOLUTION_BASE_URL="https://your-endpoint.cloud.ru/v1"
   export EVOLUTION_MODEL="your-model-name"

Затем в коде:

.. code-block:: python

   import os
   from evolution_langchain import EvolutionInference

   llm = EvolutionInference(
       model=os.getenv("EVOLUTION_MODEL"),
       key_id=os.getenv("EVOLUTION_KEY_ID"),
       secret=os.getenv("EVOLUTION_SECRET"),
       base_url=os.getenv("EVOLUTION_BASE_URL")
   )

Или используйте файл ``.env``:

.. code-block:: bash

   # .env
   EVOLUTION_KEY_ID=your_key_id
   EVOLUTION_SECRET=your_secret
   EVOLUTION_BASE_URL=https://your-endpoint.cloud.ru/v1
   EVOLUTION_MODEL=your-model-name

.. code-block:: python

   from dotenv import load_dotenv
   import os
   from evolution_langchain import EvolutionInference

   load_dotenv()

   llm = EvolutionInference(
       model=os.getenv("EVOLUTION_MODEL"),
       key_id=os.getenv("EVOLUTION_KEY_ID"),
       secret=os.getenv("EVOLUTION_SECRET"),
       base_url=os.getenv("EVOLUTION_BASE_URL")
   )

Основные возможности
--------------------

Пакетные запросы
~~~~~~~~~~~~~~~~

.. code-block:: python

   prompts = [
       "Что такое машинное обучение?",
       "Объясни принцип работы нейронных сетей",
       "Какие преимущества у Python для ML?"
   ]

   responses = llm.generate(prompts)
   for i, response in enumerate(responses.generations):
       print(f"Ответ {i + 1}: {response[0].text}")

Настройка параметров
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   llm = EvolutionInference(
       model="your-model-name",
       key_id="your_key_id",
       secret="your_secret",
       base_url="https://your-endpoint.cloud.ru/v1",
       max_tokens=1000,
       temperature=0.7,
       top_p=0.9,
       frequency_penalty=0.1,
       presence_penalty=0.1
   )

Асинхронные запросы
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from evolution_langchain import EvolutionInference

   async def main():
       llm = EvolutionInference(
           model="your-model-name",
           key_id="your_key_id",
           secret="your_secret",
           base_url="https://your-endpoint.cloud.ru/v1"
       )

       response = await llm.ainvoke("Привет! Как дела?")
       print(response)

   asyncio.run(main())

Интеграция с LangChain
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate

   # Создание шаблона
   template = "Ответь на вопрос: {question}"
   prompt = PromptTemplate(template=template, input_variables=["question"])

   # Создание цепочки
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your_key_id",
       secret="your_secret",
       base_url="https://your-endpoint.cloud.ru/v1"
   )
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение
   result = chain.run("Что такое машинное обучение?")

Обработка ошибок
~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference

   llm = EvolutionInference(
       model="your-model-name",
       key_id="your_key_id",
       secret="your_secret",
       base_url="https://your-endpoint.cloud.ru/v1"
   )

   try:
       response = llm.invoke("Привет!")
       print(response)
   except Exception as e:
       print(f"Ошибка: {e}")

Что дальше?
-----------

- Изучите :doc:`guide/basics` для подробного руководства
- Посмотрите :doc:`examples/basic` для больших примеров
- Прочитайте :doc:`api/evolution-inference` для справки по API