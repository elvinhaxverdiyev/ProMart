# 1. Python base image
FROM python:3.11-slim

# 2. Working directory
WORKDIR /app

# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy project files
COPY . /app/

# 7. Expose port (Django-nun runserver portu)
EXPOSE 8003

# 8. Start the application
CMD ["gunicorn", "order_service.wsgi:application", "--bind", "0.0.0.0:8003"]
