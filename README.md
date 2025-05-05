Promart - E-Commerce Platform Backend
Description:Promart is the backend of an e-commerce platform built with Django and Django REST Framework, based on a microservice architecture. Users can search for products, add items to their cart, process payments, and manage their accounts. Admins can manage products, orders, and user accounts. 📦💳
Key Features:

Product Catalog: Search and filter products by category. 🛒
Order Management: Add products to the cart, create orders, and track them. 📋
Payment System: Secure payments via PayPal. 💸
User Management: Registration, login, email verification, and password reset. 👤
Notifications: Real-time notifications for order status and payments (via Kafka). 🔔

Registration Process:
Users register with their email and activate their accounts using a verification code. 📧
For more details, refer to the PROJECT_OVERVIEW.md file.

Project Objectives

User Management:  

Email-based registration and verification. 🌐
Profile creation, updates, and password management. 🔐


Product Management:  

View, search, and filter product listings. 📦
Add products to the cart and place orders. 🛒


Payment Management:  

Process payments via PayPal. 💳


Notifications:  

Notify users about order and payment statuses. 🔔


Admin Management:  

Admins can manage products, orders, and user accounts. 👨‍💼



For more details, refer to the PROJECT_OVERVIEW.md file.

Technologies 🛠

Django – Web framework 🚀
Django REST Framework – For API development 📦
PostgreSQL – Database 🗄️
Celery – For asynchronous task execution ⏳
Redis – Celery broker and result storage 🔥
Kafka – Real-time messaging system 📨
JWT – User authentication 🔐
Docker – Containerized environment 🚢
PayPal SDK – Payment integration 💳


Installation and Usage
📋 Requirements

Python 3.12.5
Docker and Docker Compose
PostgreSQL (Database)
Redis (Celery Broker)
Kafka (Messaging system)

⚙️ Installation Steps

Clone the Project:
git clone https://github.com/yourusername/promart.git
cd promart


Create a Virtual Environment:
pip install pipenv
pipenv install --dev
pipenv shell


Install Required Libraries:
pipenv install


Configure the .env File:
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://postgres:your-db-password@postgres:5432/promart
REDIS_URL=redis://redis:6379/0
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_SECRET=your-paypal-secret


Build and Run Docker Containers:
docker-compose up --build


Apply Database Migrations:
docker-compose exec orders python manage.py migrate
docker-compose exec products python manage.py migrate
docker-compose exec users python manage.py migrate


Create an Admin User:
docker-compose exec users python manage.py createsuperuser



For more details, refer to the CONFIGURATION.md file.

API Endpoints

User Authentication 🔑:

/auth/register/: User registration  
/auth/login/: User login  
/auth/logout/: User logout


Product Management 📦:

/v1/products/: List all products  
/v1/products/{id}/: Product details


Order Management 🛒:

/v1/orders/cart/: Add product to cart  
/v1/orders/: Create an order


Payment Management 💳:

/v1/payments/start/: Initiate payment



For more details, refer to the API.md file.

Admin Panel Setup

Setup with Docker:
docker-compose up --build 🚀


Database Migration:
docker-compose exec users python manage.py migrate 📦


Create Superuser:
docker-compose exec users python manage.py createsuperuser 👤


Access Admin Panel:

Navigate to http://localhost:8000/admin/ and log in with superuser credentials. 🔑



For more details, refer to the ADMIN.md file.

Tests
The project includes the following test types:

Model Tests: Verify proper functioning of models (users, products, orders). 🛠️
Serializer Tests: Ensure data is serialized correctly. 📦
View Tests: Validate API responses. 🌐
Integration Tests: Test component interactions. 🔗

Running Tests
docker-compose exec users pytest

For more details, refer to the TESTS.md file.

Notes

Ensure all necessary variables (e.g., SECRET_KEY, DATABASE_URL) are correctly set in the .env file.
Pay attention to the configurations in docker-compose.yml to ensure Kafka and Redis services work correctly.

