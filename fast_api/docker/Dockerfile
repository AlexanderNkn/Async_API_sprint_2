FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["../../fast_api", "redis_elastic_waiter.sh", "./"]

RUN apt update && apt install -y netcat gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/redis_elastic_waiter.sh

ENTRYPOINT ["/usr/src/code/redis_elastic_waiter.sh"]

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
