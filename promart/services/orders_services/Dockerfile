# Bu, Django tətbiqinizin olduğu yerdəki əsas Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8003

# Kafka consumer-i burada çalıştırmaq üçün addım əlavə olunur
CMD ["sh", "-c", "python manage.py consume_products"]
