Примеры цепочек
===============

Этот раздел содержит примеры использования Evolution LangChain с LangChain цепочками.

Простая цепочка
---------------

Базовый пример создания цепочки:

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate

   # Создание шаблона
   template = "Ответь на вопрос: {question}"
   prompt = PromptTemplate(template=template, input_variables=["question"])

   # Создание LLM
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание цепочки
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение
   result = chain.run("Что такое машинное обучение?")
   print(result)

Цепочка с несколькими переменными
---------------------------------

Использование нескольких входных переменных:

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate

   # Шаблон с несколькими переменными
   template = """
   Ты - эксперт по {topic}. Ответь на вопрос подробно и информативно.
   
   Вопрос: {question}
   
   Уровень сложности: {difficulty}
   
   Ответ:"""

   prompt = PromptTemplate(
       template=template,
       input_variables=["topic", "question", "difficulty"]
   )

   # Создание LLM
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание цепочки
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение с несколькими параметрами
   result = chain.run({
       "topic": "машинное обучение",
       "question": "Что такое нейронные сети?",
       "difficulty": "начальный"
   })
   print(result)

Цепочка с форматированием
-------------------------

Использование форматирования в шаблонах:

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate

   # Шаблон с форматированием
   template = """
   # Инструкция
   
   Ты - {role}. Твоя задача: {task}
   
   ## Контекст
   {context}
   
   ## Запрос
   {request}
   
   ## Требования
   - Длина ответа: {length}
   - Стиль: {style}
   - Язык: {language}
   
   ## Ответ
   """

   prompt = PromptTemplate(
       template=template,
       input_variables=["role", "task", "context", "request", "length", "style", "language"]
   )

   # Создание LLM
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание цепочки
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение
   result = chain.run({
       "role": "эксперт по программированию",
       "task": "объяснить концепцию",
       "context": "Пользователь изучает Python",
       "request": "Что такое функции?",
       "length": "кратко",
       "style": "простой",
       "language": "русский"
   })
   print(result)

Цепочка с валидацией
--------------------

Добавление валидации входных данных:

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate
   from langchain.output_parsers import PydanticOutputParser
   from pydantic import BaseModel, Field
   from typing import List

   # Модель для валидации вывода
   class CodeExplanation(BaseModel):
       concept: str = Field(description="Название концепции")
       explanation: str = Field(description="Объяснение концепции")
       examples: List[str] = Field(description="Примеры использования")
       difficulty: str = Field(description="Уровень сложности")

   # Создание парсера
   parser = PydanticOutputParser(pydantic_object=CodeExplanation)

   # Шаблон с парсером
   template = """
   Объясни концепцию программирования в следующем формате:
   
   {format_instructions}
   
   Концепция: {concept}
   
   Объяснение:"""

   prompt = PromptTemplate(
       template=template,
       input_variables=["concept"],
       partial_variables={"format_instructions": parser.get_format_instructions()}
   )

   # Создание LLM
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Создание цепочки
   chain = LLMChain(llm=llm, prompt=prompt)

   # Выполнение с парсингом
   result = chain.run("функции")
   parsed_result = parser.parse(result)
   print(f"Концепция: {parsed_result.concept}")
   print(f"Объяснение: {parsed_result.explanation}")
   print(f"Примеры: {parsed_result.examples}")
   print(f"Сложность: {parsed_result.difficulty}")

Цепочка с обработкой ошибок
---------------------------

Добавление обработки ошибок:

.. code-block:: python

   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate
   import time

   def create_chain_with_retry():
       # Создание шаблона
       template = "Ответь на вопрос: {question}"
       prompt = PromptTemplate(template=template, input_variables=["question"])

       # Создание LLM
       llm = EvolutionInference(
           model="your-model-name",
           key_id="your-key-id",
           secret="your-secret",
           base_url="https://your-api-endpoint.com/v1"
       )

       # Создание цепочки
       chain = LLMChain(llm=llm, prompt=prompt)
       return chain

   def run_chain_with_retry(chain, question, max_retries=3):
       for attempt in range(max_retries):
           try:
               result = chain.run(question)
               return result
           except Exception as e:
               print(f"Попытка {attempt + 1} не удалась: {e}")
               if attempt < max_retries - 1:
                   time.sleep(2 ** attempt)  # Экспоненциальная задержка
               else:
                   raise e

   # Использование
   chain = create_chain_with_retry()
   
   try:
       result = run_chain_with_retry(chain, "Что такое Python?")
       print(result)
   except Exception as e:
       print(f"Все попытки не удались: {e}")

Полный пример
-------------

Объединение всех возможностей цепочек:

.. code-block:: python

   import os
   from evolution_langchain import EvolutionInference
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate

   def main():
       print("🚀 Evolution LangChain - Примеры цепочек")
       print("=" * 50)

       # Создание LLM
       llm = EvolutionInference(
           model=os.getenv("EVOLUTION_MODEL", "your-model-name"),
           key_id=os.getenv("EVOLUTION_KEY_ID", "your-key-id"),
           secret=os.getenv("EVOLUTION_SECRET", "your-secret"),
           base_url=os.getenv("EVOLUTION_BASE_URL", "https://your-api-endpoint.com/v1")
       )

       print("✅ LLM инициализирован")
       print()

       # 1. Простая цепочка
       print("1. Простая цепочка:")
       template1 = "Ответь на вопрос: {question}"
       prompt1 = PromptTemplate(template=template1, input_variables=["question"])
       chain1 = LLMChain(llm=llm, prompt=prompt1)

       try:
           result1 = chain1.run("Что такое Python?")
           print(f"Ответ: {result1}")
       except Exception as e:
           print(f"❌ Ошибка: {e}")
       print()

       # 2. Цепочка с несколькими переменными
       print("2. Цепочка с несколькими переменными:")
       template2 = """
       Ты - эксперт по {topic}. 
       Объясни концепцию '{concept}' для уровня {level}.
       
       Объяснение:"""

       prompt2 = PromptTemplate(
           template=template2,
           input_variables=["topic", "concept", "level"]
       )
       chain2 = LLMChain(llm=llm, prompt=prompt2)

       try:
           result2 = chain2.run({
               "topic": "программирование",
               "concept": "функции",
               "level": "новичок"
           })
           print(f"Ответ: {result2}")
       except Exception as e:
           print(f"❌ Ошибка: {e}")
       print()

       # 3. Цепочка с форматированием
       print("3. Цепочка с форматированием:")
       template3 = """
       # Задача
       Создай краткое описание технологии.
       
       ## Технология: {technology}
       ## Назначение: {purpose}
       
       ## Описание
       """

       prompt3 = PromptTemplate(
           template=template3,
           input_variables=["technology", "purpose"]
       )
       chain3 = LLMChain(llm=llm, prompt=prompt3)

       try:
           result3 = chain3.run({
               "technology": "Docker",
               "purpose": "контейнеризация приложений"
           })
           print(f"Ответ: {result3}")
       except Exception as e:
           print(f"❌ Ошибка: {e}")
       print()

       print("🎉 Примеры цепочек завершены!")

   if __name__ == "__main__":
       main()

Что дальше?
-----------

- Изучите :doc:`advanced` для сложных сценариев
- Прочитайте :doc:`../guide/langchain-integration` для продвинутых паттернов
- Посмотрите :doc:`../api/evolution-inference` для справки по API 