# HireIQ Backend

Django REST Framework backend for the HireIQ recruitment platform.

## Features

- Django 4.2+ with Django REST Framework 3.14+
- PostgreSQL database with connection pooling
- Environment-based settings (development, production, testing)
- Docker and Docker Compose for local development
- CORS configuration for React frontend
- API documentation with Swagger/OpenAPI
- Health check endpoint
- Comprehensive logging configuration

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (for production)

### Development Setup

1. **Clone the repository and navigate to the Django directory:**
   ```bash
   cd django
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations and setup:**
   ```bash
   python manage.py migrate
   python manage.py setup_dev
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

2. **Run setup command:**
   ```bash
   docker-compose exec web python manage.py setup_dev
   ```

3. **Access the application:**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - API Docs: http://localhost:8000/api/docs/
   - Health Check: http://localhost:8000/api/health/

## API Endpoints

### Health Check
- `GET /api/health/` - Check application health status

### Admin Interface
- `GET /admin/` - Django admin interface

### API Documentation
- `GET /api/docs/` - Swagger UI documentation
- `GET /api/schema/` - OpenAPI schema

## Environment Variables

Create a `.env` file in the Django directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=hireiq_db
DB_USER=hireiq_user
DB_PASSWORD=hireiq_password
DB_HOST=localhost
DB_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=INFO

# API Settings
API_VERSION=v1
```

## Project Structure

```
django/
├── hireiq_backend/          # Main Django project
│   ├── settings/            # Environment-based settings
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Development settings
│   │   ├── production.py   # Production settings
│   │   └── testing.py      # Testing settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI application
├── api/                     # API application
│   ├── management/         # Custom management commands
│   ├── urls.py            # API URL configuration
│   └── views.py           # API views
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── nginx.conf             # Nginx configuration
└── README.md              # This file
```

## Development Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Setup development environment
python manage.py setup_dev

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver
```

## Docker Commands

```bash
# Build and start services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Execute commands in container
docker-compose exec web python manage.py migrate
```

## Testing

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Production Deployment

1. Set `ENVIRONMENT=production` in your environment
2. Configure PostgreSQL database
3. Set up proper environment variables
4. Use Gunicorn for production server
5. Configure Nginx as reverse proxy
6. Set up SSL certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License. 