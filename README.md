# FastAPI Доска Объявлений
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/Almaz2312/fastapi_bulletin_board/blob/master/README.eng.md)
## 📌 Описание
Это сервис **'Доска Объявлений'** написанный на FastAPI.

## 🛠️ Стек технологий
- 🐍 Python 3.12
- 🔹 FastAPI
- ⚙️ Celery + Redis
- 🗄️ PostgreSQL
- 🗄️ Redis as Cache
- 🐳 Docker
- 🔗 Git для ведения версионного контроля
---

## 📥 Установка и настройка

### 🔽 Клонирование репозитория
по SSH
```bash
git clone git@github.com:Almaz2312/fastapi_bulletin_board.git
```
по HTTP
```bash
git clone https://github.com/Almaz2312/fastapi_bulletin_board.git
```
### 📦 Установка зависимостей (с использованием Poetry)
```bash
pip install poetry
poetry install --no-root
```

### ⚙️ Настройка переменных окружения
Создайте файл `.env` и укажите необходимые переменные (например, для базы данных, секретного ключа и др.). 
Пример `.env`:
```env
SECRET_KEY=YOUR_VERY_SECRET_KEY
ALGORITHM=YOUR_ALGORITHM
PROJECT_NAME=Your Project Name
PROJECT_VERSION=1.0.0
DEBUG=True

POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_user_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
```

### 📊Pytest
Use `pytest` to run tests

```bash
pytest
```

### 📊 Применение, работа с миграциями
> для автоматической генерации версионности alembic:
```bash
alembic revision --autogenerate -m "your message"
```
> сгенерировать пустую версионность alembic для заполнения в ручную:
```bash
alembic revision -m "your message"
```
> мигрировать данные в базу данных:
```bash
alembic upgrade head
```

### 🚀 Запуск сервера разработки
```bash
uvicorn app.server:api --host 0.0.0.0 --port 8000
```
### 🚀 Запуск сервера продакшена
Обычно прописываем в файле entrypoint.sh и его запускаем

---


## 🌐 Использование API
- локально `http://127.0.0.1:8000/`
- swagger `http://127.0.0.1:8000/docs`

## 🐳 Docker
### ▶️ Запуск контейнеров
```bash
docker-compose up --build -d
```
