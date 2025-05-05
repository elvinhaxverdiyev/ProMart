Tests
The Promart project uses various test types to ensure application quality.

1. Model Tests 🛠️
Verify proper functioning of models.  

Location: users/tests, products/tests, orders/tests.  
Examples:  
Validate email format in the User model.  
Test price and stock validation in the Product model.



2. API Tests 💻
Ensure API endpoints return correct responses.  

Location: users/tests, products/tests, orders/tests.  
Examples:  
Verify POST /auth/register/ creates a new user.  
Ensure GET /v1/products/ returns the product list.



3. Serializer Tests 📦
Check correct data serialization.  

Location: users/serializers, products/serializers.  
Examples:  
Validate that the Product serializer correctly formats price and stock data.



4. Integration Tests 🔗
Test component interactions.  

Location: users/tests, orders/tests.  
Examples:  
Test the full flow from registration to order creation.




Running Tests 🏃‍♂️
Locally:
pytest

With Docker:
docker-compose exec users pytest

Test Coverage 📊
To check test coverage:
pip install pytest-cov
pytest --cov=promart


Continuous Integration (CI) 🔄
Automated tests can be configured with GitHub Actions or other CI tools.
