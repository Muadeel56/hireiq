"""
Custom middleware for authentication and security
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
import time


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users using JWT tokens.
    This is a global middleware that runs before views.
    """
    
    def process_request(self, request):
        """
        Process the request and authenticate using JWT if token is present
        """
        # Skip authentication for certain paths
        exempt_paths = [
            '/api/auth/register/',
            '/api/auth/login/',
            '/api/auth/token/',
            '/api/health/',
            '/admin/',
            '/api/schema/',
            '/api/docs/',
        ]
        
        # Check if current path should be exempt
        for path in exempt_paths:
            if request.path.startswith(path):
                return None
        
        # Try to authenticate using JWT
        jwt_auth = JWTAuthentication()
        try:
            # Get the authorization header
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if auth_header.startswith('Bearer '):
                # Authenticate the request
                validated_token = jwt_auth.get_validated_token(auth_header.split(' ')[1])
                user = jwt_auth.get_user(validated_token)
                request.user = user
                
        except (InvalidToken, TokenError, IndexError):
            # If token is invalid, let the view handle it
            pass
        
        return None


class RateLimitMiddleware(MiddlewareMixin):
    """
    Custom rate limiting middleware for authentication endpoints
    """
    
    def process_request(self, request):
        """
        Check rate limits for sensitive endpoints
        """
        if not settings.RATELIMIT_ENABLE:
            return None
        
        # Define rate limits for different endpoints
        rate_limited_paths = {
            '/api/auth/login/': {'limit': 5, 'period': 300},  # 5 requests per 5 minutes
            '/api/auth/register/': {'limit': 3, 'period': 3600},  # 3 requests per hour
            '/api/auth/password-reset/': {'limit': 3, 'period': 3600},  # 3 requests per hour
        }
        
        for path, limits in rate_limited_paths.items():
            if request.path == path:
                # Create a cache key based on IP and path
                ip_address = self.get_client_ip(request)
                cache_key = f'ratelimit:{ip_address}:{path}'
                
                # Get current count
                request_count = cache.get(cache_key, 0)
                
                if request_count >= limits['limit']:
                    return JsonResponse({
                        'error': 'Too many requests. Please try again later.',
                        'retry_after': limits['period']
                    }, status=429)
                
                # Increment count
                cache.set(cache_key, request_count + 1, limits['period'])
        
        return None
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    
    def process_response(self, request, response):
        """
        Add security headers to response
        """
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
