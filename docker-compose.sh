#!/bin/bash

# HireIQ Docker Compose Management Script
# This script helps manage different Docker Compose environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
usage() {
    echo "Usage: $0 {dev|prod|test} {up|down|build|logs|shell|clean}"
    echo ""
    echo "Environments:"
    echo "  dev     - Development environment with hot-reload"
    echo "  prod    - Production environment"
    echo "  test    - Testing environment"
    echo ""
    echo "Commands:"
    echo "  up      - Start services"
    echo "  down    - Stop services"
    echo "  build   - Build services"
    echo "  logs    - Show logs"
    echo "  shell   - Open shell in backend container"
    echo "  clean   - Clean up containers, networks, and volumes"
    echo ""
    echo "Examples:"
    echo "  $0 dev up          # Start development environment"
    echo "  $0 prod build      # Build production images"
    echo "  $0 dev logs        # Show development logs"
    echo "  $0 dev shell       # Open shell in development backend"
}

# Check if enough arguments provided
if [ $# -lt 2 ]; then
    usage
    exit 1
fi

ENVIRONMENT=$1
COMMAND=$2

# Validate environment
case $ENVIRONMENT in
    dev|development)
        COMPOSE_FILE="docker-compose.yml"
        OVERRIDE_FILE="docker-compose.override.yml"
        print_info "Using development environment"
        ;;
    prod|production)
        COMPOSE_FILE="docker-compose.yml"
        OVERRIDE_FILE="infrastructure/docker/docker-compose.prod.yml"
        print_info "Using production environment"
        ;;
    test|testing)
        COMPOSE_FILE="docker-compose.yml"
        OVERRIDE_FILE="infrastructure/docker/docker-compose.test.yml"
        print_info "Using testing environment"
        ;;
    *)
        print_error "Invalid environment: $ENVIRONMENT"
        usage
        exit 1
        ;;
esac

# Compose command base (using modern Docker Compose V2)
DOCKER_COMPOSE_CMD="docker compose -f $COMPOSE_FILE"
if [ -f "$OVERRIDE_FILE" ]; then
    DOCKER_COMPOSE_CMD="$DOCKER_COMPOSE_CMD -f $OVERRIDE_FILE"
fi

# Execute commands
case $COMMAND in
    up)
        print_info "Starting $ENVIRONMENT environment..."
        $DOCKER_COMPOSE_CMD up -d
        print_success "Services started successfully!"
        print_info "Frontend: http://localhost:8080 (dev) or http://localhost (prod)"
        print_info "Backend API: http://localhost/api"
        print_info "Database: localhost:5433 (dev) or localhost:5432 (prod)"
        print_info "Redis: localhost:6379"
        ;;
    down)
        print_info "Stopping $ENVIRONMENT environment..."
        $DOCKER_COMPOSE_CMD down
        print_success "Services stopped successfully!"
        ;;
    build)
        print_info "Building $ENVIRONMENT images..."
        $DOCKER_COMPOSE_CMD build --no-cache
        print_success "Images built successfully!"
        ;;
    logs)
        print_info "Showing logs for $ENVIRONMENT environment..."
        $DOCKER_COMPOSE_CMD logs -f
        ;;
    shell)
        print_info "Opening shell in backend container..."
        $DOCKER_COMPOSE_CMD exec backend /bin/bash
        ;;
    clean)
        print_warning "This will remove all containers, networks, and volumes!"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Cleaning up..."
            $DOCKER_COMPOSE_CMD down -v --remove-orphans
            docker system prune -f
            print_success "Cleanup completed!"
        else
            print_info "Cleanup cancelled."
        fi
        ;;
    *)
        print_error "Invalid command: $COMMAND"
        usage
        exit 1
        ;;
esac 