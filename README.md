# Django E-commerce Project

A Django-based E-commerce project with user management, product listings, orders, and reviews.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Run the Development Server](#run-the-development-server)
- [Run Tests](#run-tests)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ecommerce-project.git
   cd ecommerce-project
   ```
   
2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```
   
3. **Activate the Virtual Environment:**

  - Windows:
      ```bash
      venv\Scripts\activate
      ```
    
  - Linux/Mac:
      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies:**

   ```bash
    pip install -r requirements.txt
   ```
   
5. **Database Migration:**

   ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```

6. **Project Clone & Run the Development Server:**
     ```bash
    # Python version 3.xx
   git clone https://github.com/your-username/ecommerce-project.git
   cd ecommerce-project
    cp env.example .env
    python -m venv venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic
    rm -rf static
    mv staticfiles static
    python manage.py runserver
    ```

6. **Installation (using Docker Compose): **
     ```bash
    git clone https://github.com/your-username/ecommerce-project.git
    cd ecommerce-project
    cp env.example .env
    docker-compose up --build -d
    # or
    docker-compose up --build
    ```

## Run Tests

```bash
python manage.py test
```


## API Documentation

```bash
  go to ---> http://localhost:8000/api/docs/
```
