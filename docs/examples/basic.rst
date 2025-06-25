Базовые примеры
===============

Этот раздел содержит базовые примеры использования Evolution LangChain.

Простой запрос
--------------

Самый простой способ использования:

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

Пакетная обработка
------------------

Обработка нескольких запросов одновременно:

.. code-block:: python

   from evolution_langchain import EvolutionInference

   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1"
   )

   # Список промптов
   prompts = [
       "Что такое Python?",
       "Что такое машинное обучение?",
       "Что такое искусственный интеллект?"
   ]

   # Пакетная обработка
   responses = llm.generate(prompts)

   # Вывод результатов
   for i, generation_list in enumerate(responses.generations):
       print(f"Вопрос {i+1}: {prompts[i]}")
       print(f"Ответ: {generation_list[0].text}")
       print("-" * 50)

Настройка параметров
--------------------

Пример с различными параметрами генерации:

.. code-block:: python

   from evolution_langchain import EvolutionInference

   # Создание модели с кастомными параметрами
   llm = EvolutionInference(
       model="your-model-name",
       key_id="your-key-id",
       secret="your-secret",
       base_url="https://your-api-endpoint.com/v1",
       temperature=0.7,        # Контроль случайности
       max_tokens=500,         # Максимальное количество токенов
       top_p=0.9,             # Nucleus sampling
       frequency_penalty=0.1,  # Штраф за повторения
       presence_penalty=0.1    # Штраф за присутствие
   )

   # Запрос с настроенными параметрами
   response = llm.invoke("Расскажи короткую историю о роботе")
   print(response)

Использование переменных окружения
----------------------------------

Безопасное использование учетных данных:

.. code-block:: python

   import os
   from evolution_langchain import EvolutionInference

   # Загрузка переменных окружения
   llm = EvolutionInference(
       model=os.getenv("EVOLUTION_MODEL"),
       key_id=os.getenv("EVOLUTION_KEY_ID"),
       secret=os.getenv("EVOLUTION_SECRET"),
       base_url=os.getenv("EVOLUTION_BASE_URL")
   )

   response = llm.invoke("Привет!")
   print(response)

Асинхронные запросы
-------------------

Использование асинхронных методов:

.. code-block:: python

   import asyncio
   from evolution_langchain import EvolutionInference

   async def async_example():
       llm = EvolutionInference(
           model="your-model-name",
           key_id="your-key-id",
           secret="your-secret",
           base_url="https://your-api-endpoint.com/v1"
       )

       # Асинхронный одиночный запрос
       response = await llm.ainvoke("Расскажи о квантовых компьютерах")
       print(response)

       # Асинхронная пакетная обработка
       prompts = ["Вопрос 1", "Вопрос 2", "Вопрос 3"]
       responses = await llm.agenerate(prompts)
       
       for i, generation_list in enumerate(responses.generations):
           print(f"Ответ {i+1}: {generation_list[0].text}")

   # Запуск асинхронной функции
   asyncio.run(async_example())

Обработка ошибок
----------------

Базовая обработка ошибок:

.. code-block:: python

   from evolution_langchain import EvolutionInference

   llm = EvolutionInference(
       model="your-model-name",
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

Полный пример
-------------

Объединение всех базовых возможностей:

.. code-block:: python

   import os
   from evolution_langchain import EvolutionInference

   def main():
       print("🚀 Evolution LangChain - Базовые примеры")
       print("=" * 50)

       # Инициализация модели
       llm = EvolutionInference(
           model=os.getenv("EVOLUTION_MODEL", "your-model-name"),
           key_id=os.getenv("EVOLUTION_KEY_ID", "your-key-id"),
           secret=os.getenv("EVOLUTION_SECRET", "your-secret"),
           base_url=os.getenv("EVOLUTION_BASE_URL", "https://your-api-endpoint.com/v1"),
           temperature=0.7,
           max_tokens=200
       )

       print("✅ Модель инициализирована")
       print(f"📝 Модель: {llm.model}")
       print(f"🌡️ Температура: {llm.temperature}")
       print(f"🎯 Max tokens: {llm.max_tokens}")
       print()

       # 1. Простой запрос
       print("1. Простой запрос:")
       try:
           response = llm.invoke("Привет! Расскажи о себе кратко.")
           print(f"Ответ: {response}")
       except Exception as e:
           print(f"❌ Ошибка: {e}")
       print()

       # 2. Пакетная обработка
       print("2. Пакетная обработка:")
       questions = [
           "Что такое Python?",
           "Что такое машинное обучение?"
       ]

       try:
           responses = llm.generate(questions)
           for i, response in enumerate(responses.generations):
               print(f"Вопрос {i+1}: {questions[i]}")
               print(f"Ответ: {response[0].text}")
               print()
       except Exception as e:
           print(f"❌ Ошибка: {e}")
       print()

       print("🎉 Базовые примеры завершены!")

   if __name__ == "__main__":
       main()

Что дальше?
-----------

- Изучите :doc:`chains` для примеров с LangChain цепочками
- Посмотрите :doc:`advanced` для сложных сценариев
- Прочитайте :doc:`../guide/basics` для подробного руководства 