# to install
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install poetry
poetry lock
poetry install
```


# to run locally
```bash
source .env.local
cd app
poetry run uvicorn app.main:app --host 0.0.0.0 --forwarded-allow-ips='*'
```

# to run migrations
```bash
source .env.local
poetry run alembic upgrade head
```

# to run docker mac m1
```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build
docker-compose up
```

# to run docker
```bash
docker-compose build
docker-compose up
```
check localhost:8102/docs