# HireIQ Frontend Docker Setup

This directory contains a comprehensive Docker setup for the HireIQ React frontend application with multi-stage builds supporting both development and production environments.

## 🏗️ Architecture

The Docker setup includes:

- **Multi-stage Dockerfile** with separate stages for development and production
- **Development stage** with hot-reload support using Vite dev server
- **Production stage** using Nginx to serve optimized static files
- **Security features** including non-root user execution
- **Health checks** for container monitoring
- **Environment variable injection** for runtime configuration
- **Optimized caching layers** for faster builds

## 📁 Files

- `Dockerfile` - Multi-stage Docker configuration
- `.dockerignore` - Excludes unnecessary files from build context
- `nginx.conf` - Production Nginx configuration
- `docker-entrypoint.sh` - Container initialization script
- `docker-compose.dev.yml` - Development docker-compose setup

## 🚀 Quick Start

### Development Mode

```bash
# Build and run development container
docker build --target development -t hireiq-frontend:dev .
docker run -p 5173:5173 -v $(pwd):/app -v /app/node_modules hireiq-frontend:dev

# Or use docker-compose
docker-compose -f docker-compose.dev.yml up hireiq-frontend-dev
```

### Production Mode

```bash
# Build and run production container
docker build --target production -t hireiq-frontend:prod .
docker run -p 3000:80 hireiq-frontend:prod

# Or use docker-compose
docker-compose -f docker-compose.dev.yml up hireiq-frontend-prod
```

## 🛠️ Build Stages

### 1. Base Stage
- Uses Node.js 18 Alpine for smaller image size
- Installs dumb-init for proper signal handling
- Creates non-root user for security
- Sets up working directory and copies package files

### 2. Development Stage
- Installs all dependencies including devDependencies
- Enables hot-reload with volume mounting
- Runs Vite dev server on port 5173
- Includes health check endpoint

### 3. Build Stage
- Optimized for production builds
- Uses Vite to create minified, optimized assets
- Implements code splitting and chunk optimization

### 4. Production Stage
- Uses Nginx Alpine for serving static files
- Implements comprehensive Nginx configuration
- Includes security headers and performance optimizations
- Supports SPA routing with fallback to index.html
- Runs as non-root user

## 🔧 Environment Variables

### Development
- `NODE_ENV=development`
- `REACT_APP_API_URL` - Backend API URL
- `REACT_APP_ENVIRONMENT` - Environment identifier

### Production
- `NODE_ENV=production`
- `REACT_APP_API_URL` - Backend API URL
- `REACT_APP_ENVIRONMENT` - Environment identifier

## 🏥 Health Checks

Both development and production containers include health checks:

- **Development**: `curl -f http://localhost:5173`
- **Production**: `curl -f http://localhost:80`

Additional health endpoint available at `/health` in production.

## 🔒 Security Features

- **Non-root user execution** in all stages
- **Minimal Alpine base images** for reduced attack surface
- **Security headers** in Nginx configuration
- **Proper file permissions** and ownership
- **dumb-init** for proper signal handling

## 📊 Performance Optimizations

### Build Optimizations
- **Multi-stage builds** to minimize final image size
- **Layer caching** for faster subsequent builds
- **Dependency caching** with separate package.json copy
- **Asset optimization** with Vite build tools

### Runtime Optimizations
- **Gzip compression** for all text-based assets
- **Static asset caching** with long-term cache headers
- **Chunk splitting** for better caching strategies
- **Nginx performance tuning** with optimized worker processes

## 🐳 Docker Commands

### Build Commands
```bash
# Development build
docker build --target development -t hireiq-frontend:dev .

# Production build
docker build --target production -t hireiq-frontend:prod .

# Build with build args
docker build --build-arg NODE_ENV=production -t hireiq-frontend:prod .
```

### Run Commands
```bash
# Development with volume mounting
docker run -it --rm \
  -p 5173:5173 \
  -v $(pwd):/app \
  -v /app/node_modules \
  -e REACT_APP_API_URL=http://localhost:8000/api \
  hireiq-frontend:dev

# Production
docker run -d --rm \
  -p 3000:80 \
  -e REACT_APP_API_URL=http://localhost:8000/api \
  hireiq-frontend:prod
```

### Debug Commands
```bash
# Shell into development container
docker run -it --rm hireiq-frontend:dev sh

# Shell into production container
docker run -it --rm hireiq-frontend:prod sh

# Check container logs
docker logs <container_id>
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :5173
   # Use different port
   docker run -p 3001:5173 hireiq-frontend:dev
   ```

2. **Permission issues with volumes**
   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER .
   ```

3. **Hot reload not working**
   - Ensure volume mounting is correct
   - Check that `usePolling: true` is set in vite.config.js

4. **Environment variables not working**
   - Ensure variables start with `REACT_APP_`
   - Check docker-entrypoint.sh for proper injection

### Health Check Issues
```bash
# Test health check manually
docker exec <container_id> curl -f http://localhost:5173
docker exec <container_id> curl -f http://localhost:80/health
```

## 🚀 Deployment

### Production Deployment
```bash
# Build production image
docker build --target production -t hireiq-frontend:latest .

# Tag for registry
docker tag hireiq-frontend:latest your-registry/hireiq-frontend:latest

# Push to registry
docker push your-registry/hireiq-frontend:latest
```

### Environment-specific Builds
```bash
# Staging
docker build --target production \
  --build-arg REACT_APP_ENVIRONMENT=staging \
  -t hireiq-frontend:staging .

# Production
docker build --target production \
  --build-arg REACT_APP_ENVIRONMENT=production \
  -t hireiq-frontend:production .
```

## 📝 Notes

- The Dockerfile uses Node.js 18 Alpine for optimal size and security
- Development stage supports hot-reload with proper volume mounting
- Production stage uses Nginx for optimal static file serving
- All stages run as non-root users for security
- Health checks are implemented for container orchestration
- Environment variables can be injected at runtime in production 