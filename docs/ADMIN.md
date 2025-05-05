Admin Panel Setup and Usage
This document provides information on setting up and using the Django admin panel for the Promart platform.

🚀 Admin Panel Setup 📦

Setup with Docker 🐳:
docker-compose up --build


Database Migration 🗄️:

Create Migrations ⚙️:docker-compose exec users python manage.py makemigrations


Apply Migrations 💾:docker-compose exec users python manage.py migrate




Create Superuser 👑:
docker-compose exec users python manage.py createsuperuser


Enter username, email, and password.


Access Admin Panel 🌐:

Navigate to http://localhost:8000/admin/ in your browser.
Log in with superuser credentials.


Usage ⚡:

Admin Functions: Manage users, products, orders, and payments. 📲
Admins can add, edit, or delete content. 📝❌




📋 Admin Panel Models
1. UserAdmin 👤
Manages user accounts. Admins can edit user information (name, email, status).
2. EmailVerificationAdmin 📧
Manages email verification codes. Admins can check user verification statuses.
3. DailyMessageLimitAdmin 🗓️📊
Sets daily message limits for users.
4. DailyMessageAdmin 💌
Tracks and manages daily messages sent by users.
5. CategoryAdmin 📂
Manages product categories. Admins can add or delete categories.
6. ProductAdmin 📦
Manages products. Admins can edit product names, prices, stock, and categories.
7. CartAdmin 🛒
Manages user carts. Admins can view products in carts.
8. PaymentAdmin 💳
Manages payment records. Admins can view payment statuses and details.

📌 Notes 📝:

Ensure variables like SECRET_KEY, POSTGRES_*, and JWT_* are correctly configured in the .env file. 🔒
Changes made in the admin panel directly affect platform functionality. Be cautious before confirming changes.

