# Library Management System

## Features
- User registration, JWT authentication
- Book search, borrow, return
- Admin panel for managing books and users
- PostgreSQL database
- API documentation (Swagger/Redoc)
- Docker-ready, Heroku deployable
- Filtering, pagination, security best practices
- Unit and integration tests

## Setup

1. Clone the repo and install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Configure PostgreSQL in `lib_management/db_settings.py`.
3. Run migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
5. Run the server:
   ```sh
   python manage.py runserver
   ```

## Docker

Build and run:
```sh
docker build -t library-mgmt .
docker run -p 8000:8000 library-mgmt
```

## Testing
```sh
pytest --ds=lib_management.settings
coverage run -m pytest
coverage report
```

## API Docs
- Swagger: `/swagger/`
- Redoc: `/redoc/`

## Deployment
- Configure environment variables and PostgreSQL for Heroku or your platform.
- Use `gunicorn` for production.

---
Replace all placeholder values (e.g., DB credentials) before deploying.
