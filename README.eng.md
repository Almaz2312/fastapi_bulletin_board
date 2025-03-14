# FastAPI template - Guide
[![ru](https://img.shields.io/badge/lang-ru-red.svg)](https://github.com/Almaz2312/fastapi_bulletin_board/blob/master/README.md)
## Dependencies

## 📌 Description
Service **'Bulletin Board'** is written using FastAPI.

## 🛠️ Stack
- 🐍 Python 3.x
- 🔹 FastAPI
- 🗄️ PostgreSQL
- 🗄️ Redis
- 🐳 Docker
- 🔗 Git
---

## 📥 Install and settings

### 🔽 Cloning repository
using SSH
```bash
git clone git@github.com:Almaz2312/fastapi_bulletin_board.git
```
using HTTP
```bash
git clone https://github.com/Almaz2312/fastapi_bulletin_board.git
```
### 📦 Install dependencies (using Poetry)
```bash
pip install poetry
poetry install --no-root
```

### ⚙️ Configuring your environment
Create `.env` file and write necessary environment variables (for example for your db, secret key, etc.) 
Example of `.env`:
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

Alternatively you can copy from .env.example

```bash
cp .env.example .env
```

### 📊 Use, work with alembic migrations
#### It is necessary to commit your migrations in order to avoid problems with migrations record in database abd their application
> to automatically generate alembic:
```bash
alembic revision --autogenerate -m "your message"
```
> generate empty alembic migration for manual filling:
```bash
alembic revision -m "your message"
```
> Migrate to database:
```bash
alembic upgrade head
```

### 🚀 Run server
```bash
uvicorn app.server:app --host 0.0.0.0 --port 8000
```
### 🚀 Run production server
It is a better practice to write down in entrypoint.sh and run from there

---


## 🌐 API
- local `http://127.0.0.1:8000/`
- swagger `http://127.0.0.1:8000/docs`

## 🐳 Docker
### ▶️ Run from container
```bash
docker-compose up --build -d
```
