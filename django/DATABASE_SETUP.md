# PostgreSQL Database Setup for HireIQ

This document provides comprehensive instructions for setting up and managing the PostgreSQL database for the HireIQ application.

## 🚀 Quick Start

### Prerequisites
- PostgreSQL 12+ installed
- Python 3.8+
- Virtual environment activated
- Required Python packages installed (`pip install -r requirements.txt`)

### Environment Setup
1. Copy the environment example file:
   ```bash
   cp env.example .env
   ```

2. Update the `.env` file with your PostgreSQL credentials:
   ```env
   DB_NAME=hireiq_db
   DB_USER=hireiq_user
   DB_PASSWORD=hireiq_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

### Database Creation
1. Create the database and user:
   ```bash
   sudo -u postgres createdb hireiq_db
   sudo -u postgres psql -c "CREATE USER hireiq_user WITH PASSWORD 'hireiq_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE hireiq_db TO hireiq_user;"
   sudo -u postgres psql -c "ALTER USER hireiq_user CREATEDB;"
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## 🐳 Docker Setup

### Using Docker Compose
The project includes a complete Docker Compose configuration with PostgreSQL, Django, and Nginx.

1. Start all services:
   ```bash
   docker compose up -d
   ```

2. Run migrations in the container:
   ```bash
   docker compose exec web python manage.py migrate
   ```

3. Create superuser in the container:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

### Docker Services
- **db**: PostgreSQL 15 with health checks
- **web**: Django application server
- **nginx**: Reverse proxy and static file server

## 🔧 Configuration

### Database Settings
The application supports different database configurations for different environments:

#### Development (`hireiq_backend/settings/development.py`)
- Uses environment variables with sensible defaults
- Includes Django Debug Toolbar
- No connection pooling for easier debugging

#### Production (`hireiq_backend/settings/production.py`)
- Requires all environment variables to be set
- Includes connection pooling (`CONN_MAX_AGE: 600`)
- Enhanced security settings

#### Main Settings (`hireiq_backend/settings.py`)
- Environment-based configuration using `python-decouple`
- PostgreSQL as the default database engine
- Configurable connection pooling

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_NAME` | `hireiq_db` | Database name |
| `DB_USER` | `hireiq_user` | Database user |
| `DB_PASSWORD` | `hireiq_password` | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `DB_CONN_MAX_AGE` | `0` | Connection max age (seconds) |

## 🛠️ Management Scripts

The project includes several utility scripts for database management:

### Database Backup (`scripts/db_backup.py`)
Creates timestamped backups of the PostgreSQL database.

```bash
# Create a custom format backup (recommended)
python scripts/db_backup.py

# Create a plain SQL backup
python scripts/db_backup.py --format plain

# Create a directory format backup
python scripts/db_backup.py --format directory

# List existing backups
python scripts/db_backup.py --list

# Clean up old backups (keep 10 most recent)
python scripts/db_backup.py --cleanup 10
```

### Database Restore (`scripts/db_restore.py`)
Restores database from backup files.

```bash
# List available backups
python scripts/db_restore.py --list

# Restore from a specific backup
python scripts/db_restore.py --file backups/hireiq_backup_20231213_143022.dump

# Restore with connection dropping (for active databases)
python scripts/db_restore.py --file backups/backup.dump --drop-existing
```

### Database Health Check (`scripts/db_health_check.py`)
Monitors database health and performance.

```bash
# Run basic health check
python scripts/db_health_check.py

# Verbose output with detailed information
python scripts/db_health_check.py --verbose

# JSON output for monitoring systems
python scripts/db_health_check.py --json

# Exit with error code if unhealthy (for CI/CD)
python scripts/db_health_check.py --exit-code
```

## 🏥 Health Monitoring

The health check script monitors:
- **Database Connectivity**: Connection status and response time
- **Performance Metrics**: Query latency, long-running queries, blocked queries
- **Database Information**: Version, size, active connections
- **Migration Status**: Unapplied migrations

### Health Check Output Example
```
🏥 HireIQ Database Health Check
==================================================
Timestamp: 2025-08-13 07:29:16

🔌 Database Connection:
  ✅ Database connection successful

📊 Database Information:
  Version: PostgreSQL 14.17
  Size: 9489 kB
  Active Connections: 1

⚡ Performance Metrics:
  Query Latency: ✅ 0.64ms (Excellent)
  Long Running Queries: 0
  Blocked Queries: 0

🔄 Migration Status:
  ✅ All migrations applied

==================================================
🎉 Overall Status: HEALTHY
```

## 🔒 Security Best Practices

### Production Security
1. **Use strong passwords**: Generate random passwords for production
2. **Limit connections**: Configure `max_connections` in PostgreSQL
3. **Enable SSL**: Set up SSL/TLS for database connections
4. **Regular backups**: Implement automated backup schedules
5. **Monitor access**: Enable logging and monitor database access

### Connection Security
```python
# Production database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require',  # Enable for production
            'CONN_MAX_AGE': 600,   # Connection pooling
        },
    }
}
```

## 🚨 Troubleshooting

### Common Issues

#### Connection Refused
```
psycopg2.OperationalError: could not connect to server: Connection refused
```
**Solution**: Ensure PostgreSQL is running and accepting connections on the correct port.

#### Authentication Failed
```
psycopg2.OperationalError: FATAL: password authentication failed for user
```
**Solution**: Verify username and password in environment variables.

#### Database Does Not Exist
```
psycopg2.OperationalError: FATAL: database "hireiq_db" does not exist
```
**Solution**: Create the database using `createdb` command.

#### Permission Denied
```
psycopg2.ProgrammingError: permission denied for table
```
**Solution**: Grant proper permissions to the database user.

### Diagnostic Commands
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection with psql
psql -h localhost -U hireiq_user -d hireiq_db

# Check database size and connections
sudo -u postgres psql -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) as size FROM pg_database WHERE datname = 'hireiq_db';"

# View active connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity WHERE datname = 'hireiq_db';"
```

## 📈 Performance Optimization

### Connection Pooling
Configure connection pooling for production:
```python
DATABASES = {
    'default': {
        # ... other settings
        'OPTIONS': {
            'CONN_MAX_AGE': 600,  # 10 minutes
        },
    }
}
```

### Database Indexing
Ensure proper indexing for performance:
```sql
-- Example indexes for common queries
CREATE INDEX idx_user_email ON api_user(email);
CREATE INDEX idx_created_at ON api_model(created_at);
```

### Query Optimization
- Use `select_related()` and `prefetch_related()` in Django queries
- Monitor slow queries with `pg_stat_statements`
- Use database-level constraints where possible

## 🔄 Migration Management

### Creating Migrations
```bash
# Create migrations for model changes
python manage.py makemigrations

# Create empty migration for custom SQL
python manage.py makemigrations --empty api
```

### Applying Migrations
```bash
# Apply all migrations
python manage.py migrate

# Apply migrations for specific app
python manage.py migrate api

# Show migration status
python manage.py showmigrations
```

### Rolling Back Migrations
```bash
# Rollback to specific migration
python manage.py migrate api 0001

# Show SQL for migration
python manage.py sqlmigrate api 0001
```

## 📊 Monitoring and Maintenance

### Regular Maintenance Tasks
1. **Vacuum and Analyze**: Schedule regular VACUUM and ANALYZE operations
2. **Update Statistics**: Keep table statistics up to date
3. **Monitor Disk Usage**: Check database and log file sizes
4. **Review Slow Queries**: Identify and optimize slow queries
5. **Backup Verification**: Regularly test backup restoration

### Monitoring Queries
```sql
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slow queries
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

## 📋 Checklist for Production Deployment

- [ ] PostgreSQL server configured with appropriate resources
- [ ] Database and user created with proper permissions
- [ ] SSL/TLS enabled for database connections
- [ ] Connection pooling configured
- [ ] Automated backups scheduled
- [ ] Monitoring and alerting set up
- [ ] Log rotation configured
- [ ] Security patches applied
- [ ] Performance tuning completed
- [ ] Disaster recovery plan tested

## 📞 Support

For database-related issues:
1. Check the troubleshooting section above
2. Run the health check script for diagnostics
3. Review PostgreSQL logs: `/var/log/postgresql/`
4. Consult the Django database documentation

## 📚 Additional Resources

- [Django Database Documentation](https://docs.djangoproject.com/en/stable/ref/databases/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/) 