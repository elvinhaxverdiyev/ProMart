Functionality
The core functionalities of the Promart platform are described below.

1. User Authentication and Profile Management

Registration:Users can create accounts with email, first name, last name, and password. Email verification is required to complete registration.
Login:Users log in with email and password to obtain a JWT token.
Profile:Users can update personal information (name, email) in their profiles.

2. Product Management

Catalog:Products are organized by categories (e.g., Electronics, Clothing). Each product includes a name, price, and stock.
Search and Filters:Users can search products by name, category, or price.
Product Details:Clicking a product displays its details (description, price, stock).

3. Order Management

Add to Cart:Users can add products to their cart.
Create Order:Orders can be created from cart items.
Order History:Users can view their order history.

4. Payment Integration

Payment:Users can make secure payments via PayPal.
Payment History:Users can track their payment history.

5. Notifications

Order Notifications:Real-time order status notifications are sent via Kafka.
Payment Notifications:Notifications are sent for successful or failed payments.

6. Admin Functions

Product Management:Admins can add, edit, or delete products.
User Management:Admins can view, edit, or delete user accounts.
Order Management:Admins can track and update order statuses.

