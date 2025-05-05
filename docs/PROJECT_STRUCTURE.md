Project Structure
Below is the file and folder structure of the Promart project.


promart/: Project root directory.
services/: Directory for microservices.
orders_services/: Order management service.
orders/: Models, serializers, and views for orders.
manage.py: Django management script.
requirements.txt: List of libraries.


payments_services/: Payment management service.
payments/: Payment models and PayPal integration.
manage.py: Django management script.
requirements.txt: List of libraries.


products_services/: Product management service.
products/: Product and category models, views.
manage.py: Django management script.
requirements.txt: List of libraries.


users_services/: User management service.
users/: User models, authentication, and verification.
manage.py: Django management script.
requirements.txt: List of libraries.


postgres_init/: PostgreSQL initialization scripts.


.gitignore: Files ignored by Git.
docker-compose.yml: Configuration for managing containers.
Pipfile: Python environment configuration.
Pipfile.lock: Locks library versions.
