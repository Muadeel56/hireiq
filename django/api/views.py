from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone


class HealthCheckView(APIView):
    """
    Health check endpoint for the API
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Check the health of the application
        """
        health_status = {
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0',
            'services': {
                'database': self._check_database(),
                'cache': self._check_cache(),
            }
        }
        
        # Check if all services are healthy
        all_healthy = all(
            service['status'] == 'healthy' 
            for service in health_status['services'].values()
        )
        
        if all_healthy:
            return Response(health_status, status=status.HTTP_200_OK)
        else:
            health_status['status'] = 'unhealthy'
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def _check_database(self):
        """Check database connectivity"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return {'status': 'healthy', 'message': 'Database connection successful'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': str(e)}
    
    def _check_cache(self):
        """Check cache connectivity"""
        try:
            cache.set('health_check', 'ok', 1)
            cache.get('health_check')
            return {'status': 'healthy', 'message': 'Cache connection successful'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': str(e)}


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    API information endpoint
    """
    return Response({
        'name': 'HireIQ API',
        'version': '1.0.0',
        'description': 'API for HireIQ recruitment platform',
        'endpoints': {
            'health': '/api/health/',
            'docs': '/api/schema/',
            'admin': '/admin/',
        }
    }) 