API Documentation
Below is the information about the main API endpoints of the Promart platform, organized by service (Users, Products, Orders, Payments).

Token-Related Endpoints 🚀🔑:
1. Login (Obtain Token)

URL: /login/
Method: POST
Request Payload (Content-Type: application/json):{
  "username": "string",
  "password": "string"
}


Response (200 - Content-Type: application/json):{
  "access": "string",
  "refresh": "string"
}



2. Logout

URL: /logout/
Method: POST
Request Payload (Content-Type: application/json):{}


Response (200 - Content-Type: application/json):{
  "message": "Logged out successfully."
}




User Endpoints 👤:
3. Register

URL: /register/
Method: POST
Request Payload (Content-Type: application/json):{
  "email": "user@example.com",
  "verification_code": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}


Response (201 - Content-Type: application/json):{
  "message": "Registration completed successfully."
}



4. Send Verification Code

URL: /send_verification_code/
Method: POST
Request Payload (Content-Type: application/json):{
  "email": "user@example.com"
}


Response (200 - Content-Type: application/json):



 omation of the Promart platform.

Token-Related Endpoints 🚀🔑:
1. Login (Obtain Token)

URL: /login/
Method: POST
Request Payload (Content-Type: application/json):{
  "username": "string",
  "password": "string"
}


Response (200 - Content-Type: application/json):{
  "access": "string",
  "refresh": "string"
}



2. Logout

URL: /logout/
Method: POST
Request Payload (Content-Type: application/json):{}


Response (200 - Content-Type: application/json):{
  "message": "Logged out successfully."
}




User Endpoints 👤:
3. Register

URL: /register/
Method: POST
Request Payload (Content-Type: application/json):{
  "email": "user@example.com",
  "verification_code": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}


Response (201 - Content-Type: application/json):{
  "message": "Registration completed successfully."
}



4. Send Verification Code

URL: /send_verification_code/
Method: POST
Request Payload (Content-Type: application/json):{
  "email": "user@example.com"
}


Response (200 - Content-Type: application/json):{
  "message": "Verification code sent."
}



5. Change Password

URL: /change_password/
Method: POST
Request Payload (Content-Type: application/json):{
  "old_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}


Response (200 - Content-Type: application/json):{
  "message": "Password changed successfully."
}



6. Reset Password

URL: /reset_password/
Method: POST
Request Payload (Content-Type: application/json):{
  "email": "user@example.com",
  "verification_code": "string",
  "new_password": "string",
  "confirm_password": "string"
}


Response (200 - Content-Type: application/json):{
  "message": "Password reset successfully."
}



7. Send Reset Password Code

URL: /send_code_reset_password/
Method: POST
Request Payload (Content-Type: application/json):{
  "email": "user@example.com"
}


Response (200 - Content-Type: application/json):{
  "message": "Reset password code sent."
}



8. List Users

URL: /users/
Method: GET
Response (200 - Content-Type: application/json):[
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string"
  }
]



9. User Details

URL: /users/<int:user_id>/type/
Method: GET
Response (200 - Content-Type: application/json):{
  "id": 1,
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "user_type": "string"
}




Product Endpoints 📦:
10. List Products

URL: /products/
Method: GET
Response (200 - Content-Type: application/json):[
  {
    "id": 1,
    "name": "Product Name",
    "price": "50.00",
    "category": "Electronics",
    "stock": 100
  }
]



11. Product Details

URL: /products/<int:product_id>/
Method: GET
Response (200 - Content-Type: application/json):{
  "id": 1,
  "name": "Product Name",
  "price": "50.00",
  "category": "Electronics",
  "stock": 100
}



12. List Categories

URL: /categories/
Method: GET
Response (200 - Content-Type: application/json):[
  {
    "id": 1,
    "name": "Electronics"
  }
]



13. List Subcategories

URL: /subcategories/<int:super_id>/
Method: GET
Response (200 - Content-Type: application/json):[
  {
    "id": 1,
    "name": "Smartphones",
    "super_category": 1
  }
]




Order Endpoints 🛒:
14. Toggle Cart (Add/Remove Product)

URL: /orders/cart/
Method: POST
Request Payload (Content-Type: application/json):{
  "product_id": 1,
  "quantity": 2
}


Response (201 - Content-Type: application/json):{
  "id": 1,
  "product": "Product Name",
  "quantity": 2,
  "total_price": "100.00"
}




Payment Endpoints 💳:
15. Payment Success

URL: /orders/payment/success/
Method: GET
Response (200 - Content-Type: application/json):{
  "payment_id": "PAYID-123",
  "status": "completed",
  "order_id": 1
}



16. Payment Cancel

URL: /orders/payment/cancel/
Method: GET
Response (200 - Content-Type: application/json):{
  "message": "Payment canceled.",
  "order_id": 1
}



