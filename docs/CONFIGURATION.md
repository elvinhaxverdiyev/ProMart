Installation and Configuration
This document provides detailed instructions for installing and running the Promart project.

📋 Requirements
The following software must be installed for the project to function correctly:

Python 3.12.5: For Django and other Python libraries. 🐍
Docker: For containerized environments. 🐳
Docker Compose: To manage multiple containers. ⚙️
PostgreSQL: For the database. 💾
Redis: For Celery broker and result storage. 🔄
Kafka: For real-time messaging. 📨
Django: For building the web application. 🌐
Django REST Framework (DRF): For API development. 📡
Celery: For asynchronous tasks. 🧑‍💻
JWT: For user authentication. 🔑
PayPal SDK: For payment integration. 💳


⚙️ Installation Steps

📥 Clone the Project:
git clone https://github.com/yourusername/promart.git
cd promart


🛠️ Create a Virtual Environment:
pip install pipenv
pipenv install --dev
pipenv shell


📦 Install Required Libraries:
pipenv install


🔧 Configure the .env File:Create a .env file for each service (orders, payments, products, users) and add the following parameters:
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_SETTINGS_MODULE=orders_services.settings

# PostgreSQL Configuration
DATABASE_URL=postgresql://postgres:your-db-password@postgres:5432/promart
POSTGRES_DB=promart
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_SECRET=your-paypal-secret


🐳 Build and Run Docker Containers:
docker-compose up --build


🔄 Apply Migrations:
docker-compose exec orders python manage.py migrate
docker-compose exec products python manage.py migrate
docker-compose exec users python manage.py migrate


🛡️ Create Admin User:
docker-compose exec users python manage.py createsuperuser


🧪 Run Tests (Optional):
docker-compose exec users pytest




🔍 Usage

📊 Swagger UI:Use Swagger UI to test API endpoints:

URL: http://localhost:8000/swagger/


🔗 API Endpoints:

Registration: POST /auth/register/
Login (JWT): POST /auth/login/
Product List: GET /v1/products/
Add to Cart: POST /v1/orders/cart/
Start Payment: POST /v1/payments/start/


🖥️ Admin Panel:Access the admin panel at:

http://localhost:8000/admin/




📁 Configuration Files

docker-compose.yml: Manages containers for PostgreSQL, Redis, Kafka, and Django applications.
Dockerfile: For running Django applications in containers.
Dockerfile.celery: Configuration for Celery worker containers.
Pipfile: Defines the Python environment configuration.
requirements.txt: Lists libraries for non-Pipenv users.
.env: Configuration parameters for Django, PostgreSQL, Redis, Kafka, and PayPal.

