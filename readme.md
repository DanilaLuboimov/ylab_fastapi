# Restaurant Menu

![](https://img.shields.io/badge/python-3.10-blue?style=flat-square) ![](https://img.shields.io/badge/fastapi-0.89.1-critical?style=flat-square) ![](https://img.shields.io/badge/SQLAlchemy-1.4.46-orange?style=flat-square)
![](https://img.shields.io/badge/alembic-1.9.1-yellowgreen?style=flat-square) ![](https://img.shields.io/badge/psycopg2--binary-2.9.5-9cf?style=flat-square)
![](https://img.shields.io/badge/databases-0.7.0-red?style=flat-square)

## Реализовано

1. Модели для базы данных (меню, подменю, блюда)
2. Валидация входных данных
3. Обработка данных
4. Точки доступа для взаимодействия с API
5. Создано 3 разных контейнера под разные нужды:
    1. Локальное развертывание базы
    2. Развертывание на сервере
    3. Контейнерное тестирование
6. Добавлено тестирование url доступа и логики репозиториев
7. Добавлена ручка для создания тестовых данных
8. Добавлен Celery для фонового формирования xlsx файла с общим меню
9. Подключен RabbitMQ


## Запуск (для windows)

### Подготовка

- В файле docker-compose, в строке volumes - вписываем полный путь для хранения данных
- Запустить docker desktop

### Настройка виртуального окружения

##### Команды в терминале

~~~
python -m venv venv
~~~
~~~
venv\Scripts\activate
~~~
~~~
pip install -r requirements.txt
~~~

### Локальный запуск с оперативным изменением кода проекта

##### Команды в терминале
~~~
docker-compose -f docker-compose.dev.yaml up
~~~
~~~
python main.py
~~~

##### Описание env

Для данного способа предусмотрен файл <b>.env</b>

```
● DB_USER="root"      # логин для базы данных postgresql
● DB_PASSWORD="root"  # пароль для пользователя базы данных
● DB_HOST="localhost" # доступный ip для подключения к postgresql
● DB_PORT="32700"     # открытый порт для подключения к postgresql

для локальных тестов, можно добавить следующие переменные:

●? MENU_ID="62b74c7e-5913-4fe8-a524-9e0280828c97"
●? SUBMENU_ID="cbcc0a55-8225-4053-9f71-acd65371ee9c"
●? DISH_ID="f7811d6d-bcc3-45f3-93ce-1343a7f6b34d"
```

##### Локальное тестирование
~~~
pytest -vv -W ignore::DeprecationWarning
~~~

### Запуск проекта: через docker-compose

##### Команды в терминале

~~~
docker-compose -f docker-compose.ci.yaml up
~~~
~~~
celery -A tasks.worker:worker worker --loglevel=INFO -P threads
~~~

##### Описание env

Для данного способа предусмотрен файл <b>prod.env</b>

```
● DB_USER="root"      # логин для базы данных postgresql
● DB_PASSWORD="root"  # пароль для пользователя базы данных
● PROD="db"           # наименование сервиса с postgresql
```

### Запуск docker-compose для тестирования (одна команда без регистрации)

##### Команды в терминале

~~~
docker-compose -f docker-compose.tests.yaml up  --abort-on-container-exit
~~~

Для данного способа предусмотрен файл <b>tests.env</b>

```
● DB_USER="root"                                      # логин для базы данных postgresql
● DB_PASSWORD="root"                                  # пароль для пользователя базы данных
● TESTING="db"                                        # наименование сервиса с postgresql
● MENU_ID="62b74c7e-5913-4fe8-a524-9e0280828c97"      # id для создания сущности menu и submenu в тестах
● SUBMENU_ID="cbcc0a55-8225-4053-9f71-acd65371ee9c"   # id для создания сущности submenu и dish в тестах
● DISH_ID="f7811d6d-bcc3-45f3-93ce-1343a7f6b34d"      # id для создания сущности dish в тестах
```
