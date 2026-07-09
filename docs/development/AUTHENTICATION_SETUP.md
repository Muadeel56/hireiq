# Authentication System Setup Guide

## Overview
This guide will help you set up and test the HireIQ authentication system.

## Features Implemented

✅ **JWT-based authentication** with djangorestframework-simplejwt  
✅ **User registration** with email verification  
✅ **Login/logout** functionality  
✅ **Password reset** flow  
✅ **Role-based user types** (Candidate, Recruiter, Admin)  
✅ **Protected routes** on frontend  
✅ **Authentication middleware** for API  
✅ **Rate limiting** for authentication endpoints  
✅ **Token refresh rotation** for security  

---

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
source venv/bin/activate  # or create new venv if needed
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
cp env.example .env
```

Edit `.env` with your settings:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=hireiq_db
DB_USER=hireiq_user
DB_PASSWORD=hireiq_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (for development, use console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@hireiq.com

# Frontend URL
FRONTEND_URL=http://localhost:3000

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173

# Rate Limiting
RATELIMIT_ENABLE=True
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create:
- Custom User model with email-based authentication
- UserProfile model
- JWT token blacklist tables

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### 5. Start Development Server

```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file in `frontend/` directory:

```bash
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=HireIQ
VITE_APP_ENV=development
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173` or `http://localhost:3000`

---

## Testing the Authentication System

### 1. Test User Registration

**Using curl:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!",
    "user_type": "candidate",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Expected Response:**
```json
{
  "message": "User registered successfully. Please check your email for verification.",
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "user_type": "candidate",
    "is_email_verified": false
  }
}
```

### 2. Test Email Verification

Check the console output for the verification email. The link will look like:
```
http://localhost:8000/api/auth/verify-email/VERIFICATION_TOKEN/
```

Visit the link or use curl:
```bash
curl http://localhost:8000/api/auth/verify-email/VERIFICATION_TOKEN/
```

### 3. Test User Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPassword123!"
  }'
```

**Expected Response:**
```json
{
  "message": "Login successful",
  "tokens": {
    "access": "eyJ0eXAiOiJKV1Qi...",
    "refresh": "eyJ0eXAiOiJKV1Qi..."
  },
  "user": { ... }
}
```

Save the access token for subsequent requests.

### 4. Test Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/user/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Test Token Refresh

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

### 6. Test Password Reset

**Request reset:**
```bash
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com"
  }'
```

Check console for reset email with token, then:

```bash
curl -X POST http://localhost:8000/api/auth/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "RESET_TOKEN",
    "new_password": "NewPassword123!",
    "new_password_confirm": "NewPassword123!"
  }'
```

### 7. Test Logout

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

---

## Frontend Testing

### 1. Navigate to Registration Page
Visit `http://localhost:5173/register` and create a new account.

### 2. Login
Visit `http://localhost:5173/login` and login with your credentials.

### 3. Access Protected Route
After login, navigate to `http://localhost:5173/dashboard` to verify protected routes work.

### 4. Test Logout
Click logout button to clear tokens and redirect to login.

---

## Architecture Overview

### Backend Components

1. **Models** (`api/models.py`)
   - Custom User model with email authentication
   - UserProfile for extended user information
   - Role-based user types

2. **Serializers** (`api/serializers.py`)
   - UserRegistrationSerializer
   - UserLoginSerializer
   - PasswordResetSerializer
   - EmailVerificationSerializer

3. **Views** (`api/views.py`)
   - UserRegistrationView
   - UserLoginView
   - UserLogoutView
   - EmailVerificationView
   - PasswordResetRequestView
   - PasswordResetConfirmView

4. **Middleware** (`api/middleware.py`)
   - JWTAuthenticationMiddleware
   - RateLimitMiddleware
   - SecurityHeadersMiddleware

5. **Permissions** (`api/permissions.py`)
   - IsCandidate
   - IsRecruiter
   - IsAdminUser
   - IsEmailVerified
   - IsOwnerOrReadOnly

### Frontend Components

1. **Context** (`src/contexts/AuthContext.jsx`)
   - Authentication state management
   - Login/logout functions
   - Token management

2. **Components** (`src/components/auth/`)
   - Login.jsx
   - Register.jsx
   - ForgotPassword.jsx
   - ResetPassword.jsx
   - ProtectedRoute.jsx

3. **Utilities** (`src/utils/axios.js`)
   - Axios instance with interceptors
   - Automatic token refresh

---

## Security Features

### 1. JWT Token Configuration
- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled (new refresh token on each refresh)
- **Blacklist After Rotation**: Enabled

### 2. Rate Limiting
- **Login**: 5 requests per 5 minutes per IP
- **Registration**: 3 requests per hour per IP
- **Password Reset**: 3 requests per hour per IP

### 3. Password Validation
- Minimum 8 characters
- Not too similar to user information
- Not a commonly used password
- Cannot be entirely numeric

### 4. CORS Configuration
- Configured to allow specific origins
- Credentials allowed for token management

### 5. Security Headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block

---

## Common Issues & Solutions

### Issue: ModuleNotFoundError: No module named 'django'
**Solution:** Activate virtual environment and install dependencies
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Email not sending
**Solution:** Check EMAIL_BACKEND in settings. For development, use console backend:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Issue: CORS errors on frontend
**Solution:** Ensure CORS_ALLOWED_ORIGINS includes your frontend URL:
```python
CORS_ALLOWED_ORIGINS = 'http://localhost:3000,http://localhost:5173'
```

### Issue: Token refresh not working
**Solution:** Check that token blacklist app is in INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt.token_blacklist',
    ...
]
```

### Issue: Rate limiting not working
**Solution:** Ensure cache is configured:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

---

## Next Steps

After setting up authentication:

1. ✅ Test all authentication endpoints
2. ✅ Verify email verification flow
3. ✅ Test password reset flow
4. ✅ Verify rate limiting works
5. ✅ Test protected routes on frontend
6. ✅ Verify token refresh works automatically
7. 🔄 Set up production email backend (Gmail, SendGrid, etc.)
8. 🔄 Configure proper SECRET_KEY for production
9. 🔄 Set DEBUG=False for production
10. 🔄 Configure HTTPS for production

---

## Production Checklist

Before deploying to production:

- [ ] Change SECRET_KEY to a secure random value
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up production email backend (SMTP)
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure production CORS_ALLOWED_ORIGINS
- [ ] Set up proper logging
- [ ] Enable security middleware
- [ ] Review and adjust rate limits
- [ ] Set up monitoring and alerts
- [ ] Backup database regularly
- [ ] Document API endpoints

---

## Support

For issues or questions:
1. Check the [API Documentation](/docs/api/authentication.md)
2. Review [Common Issues](#common-issues--solutions)
3. Check Django and DRF logs
4. Contact the development team

---

**Last Updated:** October 2, 2025  
**Version:** 1.0.0 