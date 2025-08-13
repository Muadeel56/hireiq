# Multi-stage Dockerfile for React Frontend
# Stage 1: Base image with Node.js
FROM node:18-alpine AS base

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create app directory and user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S reactapp -u 1001

# Set working directory
WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Stage 2: Development
FROM base AS development

# Set NODE_ENV to development
ENV NODE_ENV=development

# Install all dependencies (including devDependencies)
RUN npm ci --include=dev

# Copy source code
COPY --chown=reactapp:nodejs . .

# Switch to non-root user
USER reactapp

# Expose development port
EXPOSE 5173

# Health check for development
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5173 || exit 1

# Start development server with hot reload
CMD ["dumb-init", "npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

# Stage 3: Build stage
FROM base AS build

# Set NODE_ENV to production for optimized build
ENV NODE_ENV=production

# Install all dependencies for building
RUN npm ci --include=dev

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 4: Production with Nginx
FROM nginx:1.25-alpine AS production

# Install curl for health checks
RUN apk add --no-cache curl

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy docker entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create custom user for better security (nginx user already exists)
RUN addgroup -g 1001 -S appuser
RUN adduser -S appuser -u 1001 -G appuser

# Set proper permissions
RUN chown -R appuser:appuser /usr/share/nginx/html
RUN chown -R appuser:appuser /var/cache/nginx
RUN chown -R appuser:appuser /var/log/nginx
RUN chown -R appuser:appuser /etc/nginx/conf.d
RUN touch /var/run/nginx.pid
RUN chown -R appuser:appuser /var/run/nginx.pid

# Switch to non-root user
USER appuser

# Expose production port
EXPOSE 80

# Health check for production
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80 || exit 1

# Use entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 