from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthCheckView

router = DefaultRouter()

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('', include(router.urls)),
] 