#!/bin/sh
set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Function to inject environment variables into the built React app
inject_env_vars() {
    log "Injecting environment variables into React build..."
    
    # Define the path to the built files
    BUILD_PATH="/usr/share/nginx/html"
    
    # Check if build files exist
    if [ ! -d "$BUILD_PATH" ]; then
        log "Warning: Build path $BUILD_PATH does not exist"
        return
    fi
    
    # Find JavaScript files that might contain environment variable placeholders
    find "$BUILD_PATH" -name "*.js" -type f | while read -r file; do
        log "Processing file: $file"
        
        # Replace environment variable placeholders
        # This assumes your React app uses process.env.REACT_APP_* variables
        if [ -n "$REACT_APP_API_URL" ]; then
            sed -i "s|REACT_APP_API_URL_PLACEHOLDER|$REACT_APP_API_URL|g" "$file"
        fi
        
        if [ -n "$REACT_APP_ENVIRONMENT" ]; then
            sed -i "s|REACT_APP_ENVIRONMENT_PLACEHOLDER|$REACT_APP_ENVIRONMENT|g" "$file"
        fi
        
        # Add more environment variables as needed
        # Example:
        # if [ -n "$REACT_APP_CUSTOM_VAR" ]; then
        #     sed -i "s|REACT_APP_CUSTOM_VAR_PLACEHOLDER|$REACT_APP_CUSTOM_VAR|g" "$file"
        # fi
    done
    
    log "Environment variable injection completed"
}

# Function to validate nginx configuration
validate_nginx_config() {
    log "Validating nginx configuration..."
    if nginx -t; then
        log "Nginx configuration is valid"
    else
        log "Error: Nginx configuration is invalid"
        exit 1
    fi
}

# Function to setup nginx directories and permissions
setup_nginx() {
    log "Setting up nginx directories and permissions..."
    
    # Ensure log directories exist and have proper permissions
    mkdir -p /var/log/nginx
    mkdir -p /var/cache/nginx
    mkdir -p /var/run
    
    # Create nginx.pid if it doesn't exist
    touch /var/run/nginx.pid
    
    log "Nginx setup completed"
}

# Main execution
main() {
    log "Starting HireIQ React Frontend container..."
    log "Container user: $(whoami)"
    log "Container environment: ${NODE_ENV:-production}"
    
    # Check if we're in production mode (nginx-based)
    if [ -d "/usr/share/nginx/html" ]; then
        log "Running in production mode with nginx"
        
        # Setup nginx
        setup_nginx
        
        # Inject environment variables
        inject_env_vars
        
        # Validate nginx configuration
        validate_nginx_config
        
        log "Starting nginx server..."
    else
        log "Running in development mode"
    fi
    
    # Execute the main command
    exec "$@"
}

# Run main function
main "$@" 