FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["../../tests", "redis_elastic_waiter.sh", "pytest.ini", "./"]

RUN apt update && apt install -y netcat gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/redis_elastic_waiter.sh

ENTRYPOINT ["/usr/src/code/redis_elastic_waiter.sh"]

CMD ["pytest", "functional/src"]
