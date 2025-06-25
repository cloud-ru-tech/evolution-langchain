Интеграция с LangChain
======================

Этот раздел содержит подробное руководство по интеграции Evolution LangChain с экосистемой LangChain.

Основы интеграции
-----------------

BaseLLM наследование
~~~~~~~~~~~~~~~~~~~~

``EvolutionInference`` наследуется от ``BaseLLM`` и реализует все необходимые методы:

.. code-block:: python

    from evolution_langchain import EvolutionInference
    from langchain_core.language_models.base import BaseLLM

    # EvolutionInference является полноценным LangChain LLM
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    # Проверка совместимости
    assert isinstance(llm, BaseLLM)
    print(f"LLM тип: {llm._llm_type}")  # "cloud-ru-tech"

Стандартные методы LangChain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Синхронные методы
    response = llm.invoke("Привет!")
    responses = llm.generate(["Вопрос 1", "Вопрос 2"])

    # Асинхронные методы  
    response = await llm.ainvoke("Привет!")
    responses = await llm.agenerate(["Вопрос 1", "Вопрос 2"])

    # Streaming (если поддерживается)
    for chunk in llm.stream("Расскажи историю"):
        print(chunk, end="")

Цепочки (Chains)
----------------

LLMChain
~~~~~~~~

Базовая цепочка с промптом:

.. code-block:: python

    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate

    # Создание промпта
    template = """
    Ты - опытный программист. Ответь на следующий вопрос:

    Вопрос: {question}

    Ответ:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["question"]
    )

    # Создание цепочки
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )

    # Выполнение
    result = chain.run("Как работает замыкание в JavaScript?")
    print(result)

SimpleSequentialChain
~~~~~~~~~~~~~~~~~~~~~

Последовательное выполнение цепочек:

.. code-block:: python

    from langchain.chains import SimpleSequentialChain

    # Первая цепочка - генерация идеи
    idea_template = "Придумай идею для {topic}"
    idea_prompt = PromptTemplate(template=idea_template, input_variables=["topic"])
    idea_chain = LLMChain(llm=llm, prompt=idea_prompt)

    # Вторая цепочка - развитие идеи
    develop_template = "Развей эту идею подробнее: {idea}"
    develop_prompt = PromptTemplate(template=develop_template, input_variables=["idea"])
    develop_chain = LLMChain(llm=llm, prompt=develop_prompt)

    # Объединение в последовательную цепочку
    overall_chain = SimpleSequentialChain(
        chains=[idea_chain, develop_chain],
        verbose=True
    )

    result = overall_chain.run("мобильное приложение")

ConversationChain
~~~~~~~~~~~~~~~~~

Диалоговая цепочка с памятью:

.. code-block:: python

    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory

    # Создание памяти
    memory = ConversationBufferMemory()

    # Создание диалоговой цепочки
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    # Диалог
    response1 = conversation.predict(input="Привет! Меня зовут Алексей.")
    print(response1)

    response2 = conversation.predict(input="Как меня зовут?")
    print(response2)  # Должен помнить имя

Агенты (Agents)
---------------

ReAct агент
~~~~~~~~~~~

Агент с инструментами для решения задач:

.. code-block:: python

    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.tools import DuckDuckGoSearchRun

    # Создание инструментов
    search = DuckDuckGoSearchRun()

    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Поиск информации в интернете"
        ),
        Tool(
            name="Calculator",
            func=lambda x: str(eval(x)),
            description="Калькулятор для математических вычислений"
        )
    ]

    # Создание агента
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    # Выполнение задачи
    result = agent.run("Найди информацию о Python и вычисли 15 * 23")
    print(result)

Кастомный агент
~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.agents import BaseSingleActionAgent
    from langchain.schema import AgentAction, AgentFinish

    class CustomAgent(BaseSingleActionAgent):
        def plan(self, intermediate_steps, **kwargs):
            # Логика принятия решений агента
            user_input = kwargs.get("input", "")
            
            if "поиск" in user_input.lower():
                return AgentAction(
                    tool="Search",
                    tool_input=user_input,
                    log="Выполняю поиск"
                )
            else:
                return AgentFinish(
                    return_values={"output": f"Ответ на: {user_input}"},
                    log="Завершаю выполнение"
                )
        
        @property
        def input_keys(self):
            return ["input"]

        @property
        def output_keys(self):
            return ["output"]

    # Использование кастомного агента
    agent = CustomAgent()
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )

Векторные хранилища
-------------------

Семантический поиск
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.chains import RetrievalQA

    # Подготовка документов
    documents = [
        "Python - язык программирования общего назначения",
        "JavaScript используется для веб-разработки",
        "Machine Learning - область искусственного интеллекта"
    ]

    # Разделение текста
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.create_documents(documents)

    # Создание эмбеддингов и векторного хранилища
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    # Создание цепочки для вопросно-ответной системы
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        verbose=True
    )

    # Запрос
    result = qa_chain.run("Что такое Python?")
    print(result)

RAG (Retrieval-Augmented Generation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate

    # Кастомный промпт для RAG
    template = """
    Используй следующий контекст для ответа на вопрос:

    Контекст: {context}

    Вопрос: {question}

    Ответ на основе контекста:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # RAG цепочка с кастомным промптом
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt},
        verbose=True
    )

    result = rag_chain.run("Объясни машинное обучение")

Обработка документов
--------------------

Загрузка и обработка
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains.summarize import load_summarize_chain

    # Загрузка документа
    loader = TextLoader("document.txt")
    documents = loader.load()

    # Разделение на части
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    # Суммаризация
    summarize_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        verbose=True
    )

    summary = summarize_chain.run(texts)
    print(summary)

Анализ документов
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.chains import AnalyzeDocumentChain
    from langchain.chains.question_answering import load_qa_chain

    # Цепочка для анализа документов
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
    analyze_chain = AnalyzeDocumentChain(
        combine_docs_chain=qa_chain,
        text_splitter=text_splitter
    )

    # Анализ документа
    with open("document.txt") as f:
        content = f.read()

    result = analyze_chain.run(
        input_document=content,
        question="Какие основные темы обсуждаются в документе?"
    )

Кэширование в LangChain
-----------------------

Кэширование LLM
~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.cache import InMemoryCache
    from langchain.globals import set_llm_cache

    # Установка кэша
    set_llm_cache(InMemoryCache())

    # Теперь одинаковые запросы будут кэшироваться
    response1 = llm.invoke("Что такое Python?")
    response2 = llm.invoke("Что такое Python?")  # Из кэша

SQLite кэш
~~~~~~~~~~

.. code-block:: python

    from langchain.cache import SQLiteCache

    set_llm_cache(SQLiteCache(database_path=".langchain.db"))

    # Кэш будет сохраняться между сессиями

Callbacks и мониторинг
----------------------

Кастомные callback'и
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import LLMResult

    class CustomCallbackHandler(BaseCallbackHandler):
        def on_llm_start(self, serialized, prompts, **kwargs):
            print(f"LLM начал работу с {len(prompts)} промптами")
        
        def on_llm_end(self, response: LLMResult, **kwargs):
            print(f"LLM завершил работу, сгенерировал {len(response.generations)} ответов")
        
        def on_llm_error(self, error, **kwargs):
            print(f"Ошибка LLM: {error}")

    # Использование callback'а
    callback_handler = CustomCallbackHandler()

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        callbacks=[callback_handler]
    )

    result = chain.run("Тестовый запрос")

Интеграция с LangSmith
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from langchain.callbacks.tracers import LangChainTracer

    # Настройка LangSmith (если доступен)
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"

    # Трейсинг будет автоматическим
    tracer = LangChainTracer()

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        callbacks=[tracer]
    )

Продвинутые паттерны
--------------------

Условная генерация
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.chains import LLMChain
    from langchain.chains.base import Chain

    class ConditionalChain(Chain):
        def __init__(self, condition_chain, true_chain, false_chain):
            self.condition_chain = condition_chain
            self.true_chain = true_chain
            self.false_chain = false_chain
        
        @property
        def input_keys(self):
            return ["input"]
        
        @property  
        def output_keys(self):
            return ["output"]
        
        def _call(self, inputs):
            condition_result = self.condition_chain.run(inputs["input"])
            
            if "да" in condition_result.lower():
                result = self.true_chain.run(inputs["input"])
            else:
                result = self.false_chain.run(inputs["input"])
            
            return {"output": result}

    # Создание условных цепочек
    condition_prompt = PromptTemplate(
        template="Это вопрос о программировании? Ответь 'да' или 'нет': {input}",
        input_variables=["input"]
    )

    programming_prompt = PromptTemplate(
        template="Ответь как эксперт по программированию: {input}",
        input_variables=["input"]
    )

    general_prompt = PromptTemplate(
        template="Ответь как универсальный помощник: {input}",
        input_variables=["input"]
    )

    conditional_chain = ConditionalChain(
        condition_chain=LLMChain(llm=llm, prompt=condition_prompt),
        true_chain=LLMChain(llm=llm, prompt=programming_prompt),
        false_chain=LLMChain(llm=llm, prompt=general_prompt)
    )

Лучшие практики
---------------

Обработка ошибок
~~~~~~~~~~~~~~~~

.. code-block:: python

    from langchain.schema import OutputParserException

    try:
        result = chain.run("Некорректный ввод")
    except OutputParserException as e:
        print(f"Ошибка парсинга: {e}")
        # Повторить с другим промптом или форматом
    except Exception as e:
        print(f"Общая ошибка: {e}")
        # Логирование и обработка

Настройка параметров
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Для разных задач используйте разные настройки
    creative_llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        temperature=1.2,  # Более креативно
        max_tokens=1000
    )

    precise_llm = EvolutionInference(
        model="your-model", 
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        temperature=0.1,  # Более точно
        max_tokens=200
    )

Переиспользование
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Создайте базовую конфигурацию
    base_config = {
        "model": "your-model",
        "key_id": os.getenv("EVOLUTION_KEY_ID"),
        "secret": os.getenv("EVOLUTION_SECRET"),
        "base_url": os.getenv("EVOLUTION_BASE_URL")
    }

    # Создавайте специализированные экземпляры
    chat_llm = EvolutionInference(**base_config, temperature=0.7, max_tokens=500)
    analysis_llm = EvolutionInference(**base_config, temperature=0.1, max_tokens=1000)
    creative_llm = EvolutionInference(**base_config, temperature=1.5, max_tokens=2000)

Полный пример интеграции
------------------------

.. code-block:: python

    import os
    from evolution_langchain import EvolutionInference
    from langchain.chains import LLMChain, ConversationChain
    from langchain.prompts import PromptTemplate
    from langchain.memory import ConversationBufferMemory
    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.tools import DuckDuckGoSearchRun

    def main():
        print("🚀 Evolution LangChain - Полная интеграция")
        print("=" * 50)

        # Инициализация LLM
        llm = EvolutionInference(
            model=os.getenv("EVOLUTION_MODEL", "your-model"),
            key_id=os.getenv("EVOLUTION_KEY_ID", "your-key-id"),
            secret=os.getenv("EVOLUTION_SECRET", "your-secret"),
            base_url=os.getenv("EVOLUTION_BASE_URL", "https://your-api-endpoint.com/v1")
        )

        print("✅ LLM инициализирован")
        print()

        # 1. Простая цепочка
        print("1. Простая цепочка:")
        template = "Ответь на вопрос: {question}"
        prompt = PromptTemplate(template=template, input_variables=["question"])
        chain = LLMChain(llm=llm, prompt=prompt)

        try:
            result = chain.run("Что такое Python?")
            print(f"Ответ: {result}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

        # 2. Диалоговая цепочка
        print("2. Диалоговая цепочка:")
        memory = ConversationBufferMemory()
        conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

        try:
            conversation.predict(input="Привет! Меня зовут Анна.")
            response = conversation.predict(input="Как меня зовут?")
            print(f"Ответ: {response}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

        # 3. Агент с инструментами
        print("3. Агент с инструментами:")
        search = DuckDuckGoSearchRun()
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Поиск информации в интернете"
            )
        ]

        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False
        )

        try:
            result = agent.run("Найди информацию о Python")
            print(f"Ответ агента: {result}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

        print("🎉 Интеграция завершена!")

    if __name__ == "__main__":
        main()

Что дальше?
-----------

- Изучите :doc:`basics` для базового использования
- Прочитайте :doc:`token-management` для управления токенами
- Посмотрите :doc:`error-handling` для обработки ошибок
- Изучите :doc:`../examples/advanced` для сложных примеров 