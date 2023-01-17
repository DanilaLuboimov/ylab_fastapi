# Restaurant Menu

### Реализовано

- Модели для базы данных (меню, подменю, блюда)
- Валидация входных данных
- Обработка данных
- Точки доступа для взаимодействия с API

### Первый запуск (для windows)

#### Подготовка

- В файле docker-compose, в строке volumes - вписываем полный путь для хранения данных
- Запустить docker desktop

#### Команды в терминале

- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- docker-compose -f docker-compose.dev.yaml up
- python main.py
