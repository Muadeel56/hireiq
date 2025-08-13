from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'api'

urlpatterns = [
    # Health check
    path('health/', views.HealthCheckView.as_view(), name='health'),
    
    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('auth/verify-email/<str:token>/', views.EmailVerificationView.as_view(), name='verify-email'),
    path('auth/resend-verification/', views.resend_verification, name='resend-verification'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/password-change/', views.PasswordChangeView.as_view(), name='password-change'),
    
    # JWT token endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('user/', views.user_info, name='user-info'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user/detail/', views.UserDetailView.as_view(), name='user-detail'),
] 