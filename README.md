# Sale_bot

Имя бота @SaleForATest_bot

Последовательность действий для запуска приложения:

1. В Postgresql следует создать базу данных под названием 'sale_bot'

2. В файле settings.py, в DATABASES следует указать своё имя и пароль от postgresql

3. В терминале pycharm следует ввести последовательно следующие команды:
- python -m venv venv   (для создания виртуального окружения)
- venv\Scripts\activate.bat   (для активации виртуального окружения)
- pip install -r requirements.txt   (для установки нужных модулей)
- pip uninstall pyTelegramBotAPI
- pip install pyTelegramBotAPI==3.6.6   (без повторной загрузки модуля, приложение почему-то не работает)
- cd test_task
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

4. Зайти в файл test.py и запустить его с помощью ПКМ















