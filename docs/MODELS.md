Models
Below is information about the database models used in the Promart platform.


User 👤Description: Represents user accounts. Email is used as a unique identifier.Usage: For user registration, login, and profile management.

EmailVerification 📧Description: Stores email verification codes (email, code, timestamp).Usage: Ensures user verification during registration and password reset.

DailyMessageLimit ⏳📊Description: Defines daily message limits for users.Usage: Manages message sending limits to prevent spam.

DailyMessage 📩⏰Description: Records messages sent by users.Usage: Tracks daily message limits.

Category 📂Description: Represents product categories (e.g., Electronics, Clothing).Usage: Organizes products by category.

Product 📦Description: Represents products (name, price, stock, category).Usage: Manages the product catalog.

Cart 🛒Description: Represents user carts (product, quantity, total price).Usage: For adding products to the cart and creating orders.

Payment 💳Description: Stores payment records (order, amount, status).Usage: Tracks and manages payments.


