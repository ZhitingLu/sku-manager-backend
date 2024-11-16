# Medication SKU API

A RESTful API to manage medication SKUs, allowing users to perform CRUD operations and bulk-upload medication SKUs to the catalogue. This project meets the requirements to manage medication SKUs via APIs and supports authentication, user-specific data, and bulk operations.

## Features

- **CRUD Operations**: 
  - Create, Read, Update, and Delete individual medication SKU through dedicated APIs.
- **Bulk Create**: 
  - A dedicated API to bulk create multiple medication SKUs.
- **User Authentication**: 
  - Users must be authenticated to interact with the API.
- **Role-based Access Control**: 
  - Only authenticated users can partial/full update and delete the medication SKUs.
- **API Documentation**: 
  - Detailed descriptions of each API endpoint.
- **GitHub Actions for CI/CD**:
  - Code Quality Checks: Automatically run linter and formatter on every push or pull request.
  - Unit and Integration Tests: Run automated tests using Python test framework to ensure code reliability

## 🚀 Tech Stack
- **🌐 Django**: A high-level web framework for rapid and secure development.
- **📖 Django REST Framework (DRF)**: Toolkit for building robust and scalable Web APIs.
- **✨ DRF-Spectacular**: A customizable OpenAPI 3.0 generator for DRF.
- **🐘 PostgreSQL**: A powerful open-source database used to store medication SKUs.
- **🔒 Django Authentication**: Provides token-based authentication for user access.
- **🐳 Docker**: A platform for developing, shipping, and running applications in containers.

## Prerequisites

Make sure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/engine/install/)

## Setup & Installation

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
# SSH
git clone git@github.com:ZhitingLu/medication_sku.git
cd medication-sku
```

### 2. Build and Run the Application with Docker
Step 1: Build the Docker Container

```bash
# bash
docker compose build
```

Step 2: Start the Application

```bash
# bash
docker compose up
```

### 3. Apply Migrations
After starting the application, open another terminal and run (just in case):

```bash
# bash
docker compose run --rm app sh -c "python manage.py migrate"
```

### 4. Access the Application
API: The application will be available at http://localhost:8000/.
Admin Panel: Visit http://localhost:8000/admin/ to access the admin panel.

### 🧪 Running Tests
Run the following command to execute tests:

```bash
# bash
docker compose run --rm app sh -c "python manage.py test && flake8"
```

### 📂 Folder Structure
```
.
├── .github/               # GitHub Actions
│   ├── workflows/         # Workflows
├── app/                   # Main Django application code
│   ├── app/               # Main app for configurations and settings
│   ├── core/              # Core app containing foundational models
│   ├── user/              # Custom user management app
│   ├── medication_sku/    # Medication SKU API app
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker build instructions
├── requirements.txt       # Production dependencies
├── requirements.dev.txt   # Development dependencies
```

### 📖 API Documentation
API documentation is automatically generated using DRF-Spectacular. After running the application, visit:

Swagger UI: http://localhost:8000/api/docs/
Download schema: http://localhost:8000/api/schema/

![img.png](img.png)

### 🔧 Common Commands
- Run Migrations: 
```
docker compose run --rm app sh -c "python manage.py migrate"
```
- Create Superuser: 
```
docker compose run --rm app sh -c "python manage.py createsuperuser"
```
- Install New Dependencies: Add them to requirements.txt and rebuild the container:
```
docker compose build
```

### How to test the APIs as an authenticated user
When the application is running, please head to the Swagger UI: http://localhost:8000/api/docs/

Step 1: create a user

![create_user](https://github.com/user-attachments/assets/a79dc5fc-c495-4f2a-a1e4-e0fbe981f4e7)

Step 2: Login the user with the creadentials just created

![login_user](https://github.com/user-attachments/assets/9fe77f6d-e43c-4d9f-917e-4de5ac83ec66)

Step 3: Copy the returned token value

![user_token](https://github.com/user-attachments/assets/e3e53b7e-6990-4370-8513-50bdc97b432d)


Step 4: Authorize the user

![authorize_user](https://github.com/user-attachments/assets/3fa1bc6e-e5dd-41a2-b954-ba595db8231f)


Pass the token copied from Step 3 with 'Token ' in front

![pass_token](https://github.com/user-attachments/assets/ca083b05-5a69-4f3c-9200-a643c2756495)


Step 5: Create a new medication sku as an authenticated user

![create_sku](https://github.com/user-attachments/assets/c6a48d7d-66be-4705-ba7e-37cbfb350262)


Created:
![sku_created](https://github.com/user-attachments/assets/a832b464-e766-40ac-8b76-e0a6a465a5e2)

## Updates:
1. Added 'tags' API endpoints
2. Nested '/medication_skus/' and '/tags/' endpoints inside '/medication_sku/':
 ![image](https://github.com/user-attachments/assets/7750662e-8f1e-49c7-92ac-19b84e38f54f)








