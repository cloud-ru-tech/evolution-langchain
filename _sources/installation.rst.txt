Установка
=========

Evolution LangChain можно установить несколькими способами.

Требования к системе
--------------------

- Python 3.8.1 или выше
- pip или Poetry для управления пакетами

Установка через pip
-------------------

Самый простой способ установки:

.. code-block:: bash

   pip install evolution-langchain

Установка через Poetry
----------------------

Если вы используете Poetry для управления зависимостями:

.. code-block:: bash

   poetry add evolution-langchain

Установка из исходного кода
---------------------------

Для разработчиков или для получения последней версии:

.. code-block:: bash

   git clone https://github.com/your-repo/evolution-langchain.git
   cd evolution-langchain
   pip install -e .

Установка для разработки
------------------------

Если вы планируете вносить изменения в код:

.. code-block:: bash

   git clone https://github.com/your-repo/evolution-langchain.git
   cd evolution-langchain
   
   # С Poetry
   poetry install --with=dev,docs
   
   # Или с pip
   pip install -e ".[dev,test,docs]"

Проверка установки
------------------

Проверьте, что установка прошла успешно:

.. code-block:: python

   import evolution_langchain
   print(evolution_langchain.__version__)

Или через командную строку:

.. code-block:: bash

   python -c "import evolution_langchain; print(evolution_langchain.__version__)"

Обновление
----------

Для обновления до последней версии:

.. code-block:: bash

   # С pip
   pip install --upgrade evolution-langchain
   
   # С Poetry
   poetry update evolution-langchain

Удаление
--------

Если нужно удалить пакет:

.. code-block:: bash

   # С pip
   pip uninstall evolution-langchain
   
   # С Poetry (удалить из проекта)
   poetry remove evolution-langchain

Зависимости
-----------

Основные зависимости:

- **langchain-core** - Основная библиотека LangChain
- **requests** - HTTP клиент для API запросов
- **pydantic** - Валидация данных
- **typing-extensions** - Расширения типов

Опциональные зависимости:

- **python-dotenv** - Загрузка переменных окружения из .env файлов
- **aiohttp** - Асинхронные HTTP запросы

Настройка окружения
-------------------

Переменные окружения
~~~~~~~~~~~~~~~~~~~~

Создайте файл `.env` в корне вашего проекта:

.. code-block:: bash

   # .env
   EVOLUTION_KEY_ID=your_key_id
   EVOLUTION_SECRET=your_secret
   EVOLUTION_BASE_URL=https://your-endpoint.cloud.ru/v1
   EVOLUTION_MODEL=your-model-name

Или установите переменные окружения в системе:

.. code-block:: bash

   export EVOLUTION_KEY_ID="your_key_id"
   export EVOLUTION_SECRET="your_secret"
   export EVOLUTION_BASE_URL="https://your-endpoint.cloud.ru/v1"
   export EVOLUTION_MODEL="your-model-name"

Возможные проблемы
------------------

Конфликт версий Python
~~~~~~~~~~~~~~~~~~~~~~

Если вы получаете ошибку о несовместимости версий Python:

.. code-block:: bash

   ERROR: evolution-langchain requires Python '>=3.8.1' but the running Python is 3.8.0

Обновите Python до версии 3.8.1 или выше.

Проблемы с зависимостями
~~~~~~~~~~~~~~~~~~~~~~~~

При конфликтах зависимостей попробуйте:

.. code-block:: bash

   # Очистить кеш pip
   pip cache purge
   
   # Переустановить пакет
   pip uninstall evolution-langchain
   pip install evolution-langchain

Проблемы с установкой в виртуальном окружении
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Убедитесь, что виртуальное окружение активировано:

.. code-block:: bash

   # Создание виртуального окружения
   python -m venv venv
   
   # Активация (Linux/Mac)
   source venv/bin/activate
   
   # Активация (Windows)
   venv\Scripts\activate
   
   # Установка
   pip install evolution-langchain

Проблемы с правами доступа
~~~~~~~~~~~~~~~~~~~~~~~~~~

Если возникают проблемы с правами доступа:

.. code-block:: bash

   # Установка с флагом --user
   pip install --user evolution-langchain
   
   # Или с sudo (не рекомендуется)
   sudo pip install evolution-langchain

Что дальше?
-----------

- Изучите :doc:`quickstart` для быстрого старта
- Прочитайте :doc:`guide/basics` для подробного руководства
- Посмотрите :doc:`examples/basic` для примеров использования 