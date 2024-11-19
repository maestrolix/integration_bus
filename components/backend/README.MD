# Развертывание проекта

## 1. Установка зависимостей

В директории /components/backend/, прописать следующие команды:

```text
python3 -m venv .venv
source env/bin/activate
pip install -r requirements.txt
```

## 2. Применение миграций к БД

В директории /components/backend/, прописать следующую команду:

```text
python -m integration_bus.composites.alembic_runner upgrade head
```

## 3. Создание миграций (опционально)

В директории /components/backend/, прописать следующую команду:

```text
python -m integration_bus.composites.alembic_runner revision --autogenerate -m 'your_name'
```

## 4. Откат миграций (опционально)

В директории /components/backend/, прописать следующую команду:

```text
python -m integration_bus.composites.alembic_runner downgrade -[1-N]
```

## 5. Запуск http-сервера (DEV)

В директории /components/backend/, прописать следующую команду:

```text
uvicorn integration_bus.composites.http_api:app --reload --port 5002 --host 0.0.0.0
```

## 6. Запуск http-сервера (PROD)

В директории /components/backend/, прописать следующую команду:

```text
gunicorn integration_bus.composites.http_api:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5002
```

# DEPLOYMENT

## 1. DEV

В директории /components/deployment/docker-compose, прописать следующую команду:

```docker
sudo docker compose -f dev.yml --env-file .env.dev up --build -d
```

или

```docker
sudo docker-compose -f dev.yml --env-file .env.dev up --build -d
```

## 2. PROD

```docker
sudo docker compose -f prod.yml --env-file .env.prod up --build -d
```

или

```docker
sudo docker-compose -f prod.yml --env-file .env.prod up --build -d
```
