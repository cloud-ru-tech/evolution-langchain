Продвинутые примеры
===================

Этот раздел содержит сложные примеры использования Evolution LangChain для решения практических задач.

RAG система с документами
-------------------------

Создание системы вопросов-ответов на основе загруженных документов:

.. code-block:: python

    from evolution_langchain import EvolutionInference
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate

    # Инициализация LLM
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1",
        temperature=0.3,  # Низкая температура для точности
        max_tokens=800
    )

    # Загрузка и обработка документов
    def create_rag_system(document_paths):
        # Загрузка документов
        documents = []
        for path in document_paths:
            loader = TextLoader(path, encoding='utf-8')
            documents.extend(loader.load())
        
        # Разделение на чанки
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_documents(documents)
        
        # Создание векторного хранилища
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        vectorstore = FAISS.from_documents(texts, embeddings)
        
        # Кастомный промпт
        template = """
        Используй следующий контекст для ответа на вопрос. Если информации в контексте недостаточно, скажи об этом.
        
        Контекст:
        {context}
        
        Вопрос: {question}
        
        Подробный ответ:"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Создание RAG цепочки
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        return qa_chain

    # Использование
    document_paths = ["doc1.txt", "doc2.txt", "doc3.txt"]
    rag_system = create_rag_system(document_paths)

    query = "Какие основные преимущества использования Python?"
    result = rag_system({"query": query})

    print(f"Вопрос: {query}")
    print(f"Ответ: {result['result']}")
    print(f"Источники: {[doc.metadata for doc in result['source_documents']]}")

Мультиагентная система
----------------------

Система из нескольких специализированных агентов:

.. code-block:: python

    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.memory import ConversationBufferMemory
    from langchain.schema import BaseOutputParser
    import requests

    class SpecializedAgent:
        def __init__(self, name, system_prompt, llm):
            self.name = name
            self.system_prompt = system_prompt
            self.llm = llm
            
            # Создание промпта с системным сообщением
            from langchain.prompts import PromptTemplate
            
            template = f"""
            {system_prompt}
            
            Человек: {{input}}
            Ассистент:"""
            
            self.prompt = PromptTemplate(
                template=template,
                input_variables=["input"]
            )
        
        def process(self, input_text):
            formatted_prompt = self.prompt.format(input=input_text)
            return self.llm.invoke(formatted_prompt)

    # Создание специализированных агентов
    code_agent = SpecializedAgent(
        name="CodeExpert",
        system_prompt="Ты - эксперт по программированию. Отвечай только на вопросы о коде, алгоритмах и технологиях.",
        llm=llm
    )

    math_agent = SpecializedAgent(
        name="MathExpert", 
        system_prompt="Ты - математик. Решай математические задачи и объясняй математические концепции.",
        llm=llm
    )

    general_agent = SpecializedAgent(
        name="GeneralAssistant",
        system_prompt="Ты - универсальный помощник. Отвечай на общие вопросы.",
        llm=llm
    )

    class AgentRouter:
        def __init__(self, agents, classifier_llm):
            self.agents = agents
            self.classifier = classifier_llm
        
        def route(self, query):
            # Классификация запроса
            classification_prompt = f"""
            Определи категорию следующего вопроса:
            
            Вопрос: {query}
            
            Категории:
            - code: вопросы о программировании, коде, алгоритмах
            - math: математические задачи и вопросы
            - general: общие вопросы
            
            Ответь только названием категории:"""
            
            category = self.classifier.invoke(classification_prompt).strip().lower()
            
            # Выбор агента
            if "code" in category:
                return self.agents["code"]
            elif "math" in category:
                return self.agents["math"]
            else:
                return self.agents["general"]
        
        def process(self, query):
            selected_agent = self.route(query)
            print(f"🎯 Выбран агент: {selected_agent.name}")
            return selected_agent.process(query)

    # Создание роутера
    agents = {
        "code": code_agent,
        "math": math_agent,
        "general": general_agent
    }

    router = AgentRouter(agents, llm)

    # Тестирование
    queries = [
        "Как реализовать быструю сортировку на Python?",
        "Вычисли производную функции f(x) = x^2 + 3x + 2",
        "Какая погода в Москве?"
    ]

    for query in queries:
        print(f"\n📝 Запрос: {query}")
        response = router.process(query)
        print(f"💬 Ответ: {response}")

Система с памятью и контекстом
------------------------------

Создание системы с долгосрочной памятью:

.. code-block:: python

    from evolution_langchain import EvolutionInference
    from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
    from langchain.chains import ConversationChain
    from langchain.prompts import PromptTemplate

    # Инициализация LLM
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    # Создание памяти с суммаризацией
    memory = ConversationSummaryMemory(llm=llm)

    # Кастомный промпт для диалога
    template = """
    Ты - полезный ассистент с памятью о предыдущих разговорах.
    
    История разговора:
    {history}
    
    Человек: {input}
    Ассистент:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["history", "input"]
    )

    # Создание цепочки с памятью
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )

    # Диалог
    responses = []
    messages = [
        "Привет! Меня зовут Алексей.",
        "Я программист и изучаю Python.",
        "Какие книги по Python ты можешь порекомендовать?",
        "А что насчет машинного обучения?",
        "Как меня зовут и чем я занимаюсь?"
    ]

    for message in messages:
        response = conversation.predict(input=message)
        responses.append(response)
        print(f"Человек: {message}")
        print(f"Ассистент: {response}")
        print("-" * 50)

Система мониторинга и логирования
---------------------------------

Создание системы с детальным мониторингом:

.. code-block:: python

    import time
    import logging
    from dataclasses import dataclass
    from typing import List, Optional
    from evolution_langchain import EvolutionInference

    @dataclass
    class RequestMetrics:
        prompt: str
        response: str
        duration: float
        tokens_used: Optional[int] = None
        success: bool = True
        error: Optional[str] = None

    class MonitoredEvolutionInference:
        def __init__(self, llm):
            self.llm = llm
            self.metrics: List[RequestMetrics] = []
            
            # Настройка логирования
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        
        def invoke(self, prompt):
            start_time = time.time()
            
            try:
                response = self.llm.invoke(prompt)
                duration = time.time() - start_time
                
                # Оценка количества токенов
                estimated_tokens = (len(prompt) + len(response)) // 4
                
                metric = RequestMetrics(
                    prompt=prompt[:100],  # Первые 100 символов
                    response=response[:100],
                    duration=duration,
                    tokens_used=estimated_tokens,
                    success=True
                )
                
                self.metrics.append(metric)
                self.logger.info(f"Запрос выполнен за {duration:.2f}с")
                return response
                
            except Exception as e:
                duration = time.time() - start_time
                
                metric = RequestMetrics(
                    prompt=prompt[:100],
                    response="",
                    duration=duration,
                    success=False,
                    error=str(e)
                )
                
                self.metrics.append(metric)
                self.logger.error(f"Ошибка запроса за {duration:.2f}с: {e}")
                raise
        
        def get_stats(self):
            """Получение статистики использования."""
            if not self.metrics:
                return "Нет данных"
            
            total_requests = len(self.metrics)
            successful_requests = sum(1 for m in self.metrics if m.success)
            avg_duration = sum(m.duration for m in self.metrics) / total_requests
            total_tokens = sum(m.tokens_used or 0 for m in self.metrics)
            
            return {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "success_rate": successful_requests / total_requests * 100,
                "avg_duration": avg_duration,
                "total_estimated_tokens": total_tokens
            }

    # Использование
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    monitored_llm = MonitoredEvolutionInference(llm)

    # Выполнение запросов
    questions = ["Что такое ИИ?", "Что такое ML?", "Что такое DL?"]
    
    for question in questions:
        try:
            response = monitored_llm.invoke(question)
            print(f"Q: {question}")
            print(f"A: {response[:100]}...")
            print("-" * 50)
        except Exception as e:
            print(f"Ошибка для вопроса '{question}': {e}")

    # Просмотр статистики
    stats = monitored_llm.get_stats()
    print(f"Статистика: {stats}")

Система кэширования
-------------------

Реализация системы кэширования:

.. code-block:: python

    import hashlib
    import json
    import os
    from evolution_langchain import EvolutionInference

    class CacheManager:
        def __init__(self, cache_dir="llm_cache"):
            self.cache_dir = cache_dir
            os.makedirs(cache_dir, exist_ok=True)
        
        def _get_cache_key(self, prompt, **kwargs):
            """Создание ключа кэша на основе промпта и параметров."""
            cache_data = {"prompt": prompt, **kwargs}
            cache_string = json.dumps(cache_data, sort_keys=True)
            return hashlib.md5(cache_string.encode()).hexdigest()
        
        def get(self, prompt, **kwargs):
            """Получение из кэша."""
            key = self._get_cache_key(prompt, **kwargs)
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)["response"]
            return None
        
        def set(self, prompt, response, **kwargs):
            """Сохранение в кэш."""
            key = self._get_cache_key(prompt, **kwargs)
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            
            cache_data = {
                "prompt": prompt,
                "response": response,
                "params": kwargs
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)

    class CachedEvolutionInference:
        def __init__(self, llm, cache_manager):
            self.llm = llm
            self.cache = cache_manager
        
        def invoke(self, prompt, **kwargs):
            # Проверить кэш
            cached_response = self.cache.get(prompt, **kwargs)
            if cached_response:
                print("📦 Ответ из кэша")
                return cached_response
            
            # Выполнить запрос
            print("🌐 Запрос к API")
            response = self.llm.invoke(prompt)
            
            # Сохранить в кэш
            self.cache.set(prompt, response, **kwargs)
            
            return response

    # Использование
    llm = EvolutionInference(
        model="your-model",
        key_id="your-key-id",
        secret="your-secret",
        base_url="https://your-api-endpoint.com/v1"
    )

    cache_manager = CacheManager()
    cached_llm = CachedEvolutionInference(llm, cache_manager)

    # Первый запрос - к API
    response1 = cached_llm.invoke("Что такое Python?")
    print(response1)

    # Второй запрос - из кэша
    response2 = cached_llm.invoke("Что такое Python?")
    print(response2)

Полный пример
-------------

Объединение всех продвинутых возможностей:

.. code-block:: python

    import os
    from evolution_langchain import EvolutionInference
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationSummaryMemory

    def main():
        print("🚀 Evolution LangChain - Продвинутые примеры")
        print("=" * 60)

        # Инициализация LLM
        llm = EvolutionInference(
            model=os.getenv("EVOLUTION_MODEL", "your-model-name"),
            key_id=os.getenv("EVOLUTION_KEY_ID", "your-key-id"),
            secret=os.getenv("EVOLUTION_SECRET", "your-secret"),
            base_url=os.getenv("EVOLUTION_BASE_URL", "https://your-api-endpoint.com/v1")
        )

        print("✅ LLM инициализирован")
        print()

        # 1. Система с памятью
        print("1. Система с памятью:")
        memory = ConversationSummaryMemory(llm=llm)
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )

        try:
            conversation.predict(input="Привет! Меня зовут Иван.")
            conversation.predict(input="Я изучаю машинное обучение.")
            response = conversation.predict(input="Что ты знаешь обо мне?")
            print(f"Ответ: {response}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

        # 2. Мультиагентная система
        print("2. Мультиагентная система:")
        from langchain.prompts import PromptTemplate

        class SimpleAgent:
            def __init__(self, name, system_prompt, llm):
                self.name = name
                template = f"{system_prompt}\n\nВопрос: {{input}}\nОтвет:"
                self.prompt = PromptTemplate(template=template, input_variables=["input"])
                self.llm = llm
            
            def process(self, input_text):
                formatted_prompt = self.prompt.format(input=input_text)
                return self.llm.invoke(formatted_prompt)

        code_agent = SimpleAgent(
            "CodeExpert",
            "Ты - эксперт по программированию.",
            llm
        )

        try:
            response = code_agent.process("Как создать функцию в Python?")
            print(f"Ответ эксперта по коду: {response}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

        # 3. Система мониторинга
        print("3. Система мониторинга:")
        import time

        class SimpleMonitor:
            def __init__(self, llm):
                self.llm = llm
                self.requests = 0
                self.total_time = 0
            
            def invoke(self, prompt):
                start_time = time.time()
                try:
                    response = self.llm.invoke(prompt)
                    duration = time.time() - start_time
                    self.requests += 1
                    self.total_time += duration
                    print(f"✅ Запрос {self.requests} выполнен за {duration:.2f}с")
                    return response
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
                    raise

        monitored_llm = SimpleMonitor(llm)

        try:
            monitored_llm.invoke("Расскажи анекдот")
            monitored_llm.invoke("Что такое ИИ?")
            print(f"📊 Среднее время: {monitored_llm.total_time/monitored_llm.requests:.2f}с")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

        print("🎉 Продвинутые примеры завершены!")

    if __name__ == "__main__":
        main()

Что дальше?
-----------

- Изучите :doc:`../guide/langchain-integration` для продвинутых паттернов интеграции
- Прочитайте :doc:`../guide/token-management` для понимания управления токенами
- Посмотрите :doc:`../api/evolution-inference` для полной документации API 