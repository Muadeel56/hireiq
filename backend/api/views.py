from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
import json

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, PasswordChangeSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, EmailVerificationSerializer
)


class HealthCheckView(APIView):
    """
    Health check endpoint for the API
    """
    permission_classes = [permissions.AllowAny]
    
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


class UserRegistrationView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate email verification token
            token = get_random_string(64)
            user.email_verification_token = token
            user.save()
            
            # Send verification email (in production, use proper email service)
            verification_url = f"http://localhost:8000/api/auth/verify-email/{token}/"
            send_mail(
                'Verify your email - HireIQ',
                f'Click the following link to verify your email: {verification_url}',
                'noreply@hireiq.com',
                [user.email],
                fail_silently=True,
            )
            
            return Response({
                'message': 'User registered successfully. Please check your email for verification.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    User login endpoint.
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """
    Email verification endpoint.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            
            return Response({
                'message': 'Email verified successfully'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid verification token'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """
    Password reset request endpoint.
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = get_random_string(64)
            user.email_verification_token = token
            user.save()
            
            # Send reset email
            reset_url = f"http://localhost:3000/reset-password/{token}"
            send_mail(
                'Password Reset - HireIQ',
                f'Click the following link to reset your password: {reset_url}',
                'noreply@hireiq.com',
                [email],
                fail_silently=True,
            )
            
            return Response({
                'message': 'Password reset email sent'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    Password reset confirmation endpoint.
    """
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'auth'
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email_verification_token=token)
                user.set_password(new_password)
                user.email_verification_token = None
                user.save()
                
                return Response({
                    'message': 'Password reset successful'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view and update.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user.profile


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    User detail view and update.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """
    Password change endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    """
    Get current user information.
    """
    return Response(UserSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def resend_verification(request):
    """
    Resend email verification.
    """
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        if user.is_email_verified:
            return Response({'error': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new verification token
        token = get_random_string(64)
        user.email_verification_token = token
        user.save()
        
        # Send verification email
        verification_url = f"http://localhost:8000/api/auth/verify-email/{token}/"
        send_mail(
            'Verify your email - HireIQ',
            f'Click the following link to verify your email: {verification_url}',
            'noreply@hireiq.com',
            [user.email],
            fail_silently=True,
        )
        
        return Response({'message': 'Verification email sent'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 