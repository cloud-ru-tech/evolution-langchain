.. Evolution LangChain documentation master file, created by
   sphinx-quickstart on Tue Dec 19 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Evolution LangChain Documentation
=================================

.. image:: https://img.shields.io/pypi/v/evolution-langchain.svg
   :target: https://pypi.org/project/evolution-langchain/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/evolution-langchain.svg
   :target: https://pypi.org/project/evolution-langchain/
   :alt: Python versions

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

**Evolution LangChain** - это современная интеграция Evolution Inference API с экосистемой LangChain, обеспечивающая автоматическое управление токенами доступа и полную совместимость с OpenAI API.

Особенности
-----------

✅ **Автоматическое управление токенами** - Автоматическое получение и обновление access_token с буферизацией и thread-safe операциями

✅ **Совместимость с OpenAI API** - Полная совместимость с форматом OpenAI API для легкой миграции существующих проектов

✅ **Нативная интеграция с LangChain** - Работает со всеми компонентами LangChain: цепочками, агентами, векторными хранилищами

✅ **Thread-safe** - Безопасное использование в многопоточных приложениях с автоматической синхронизацией

✅ **Автоматическое восстановление** - Автоматическое обновление токенов при истечении срока с обработкой ошибок

✅ **Простота использования** - Минимальная настройка, максимальная функциональность из коробки

Быстрый старт
-------------

Установка
~~~~~~~~~

.. code-block:: bash

   pip install evolution-langchain

Основное использование
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from evolution_langchain import EvolutionInference

   # Инициализация модели
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Простой запрос
   response = llm.invoke("Привет! Как дела?")
   print(response)

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
       model="your-model",
       key_id="your-key-id", 
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение
   result = chain.run("Что такое машинное обучение?")

Содержание
----------

.. toctree::
   :maxdepth: 2
   :caption: Руководство пользователя:

   quickstart
   installation
   guide/basics
   guide/langchain-integration
   guide/token-management
   guide/error-handling

.. toctree::
   :maxdepth: 2
   :caption: Примеры:

   examples/basic
   examples/chains
   examples/advanced

.. toctree::
   :maxdepth: 2
   :caption: API документация:

   api/evolution-inference
   api/token-manager

Индексы и таблицы
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 