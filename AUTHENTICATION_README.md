# 🔐 HireIQ Authentication System

## Implementation Summary

This document summarizes the implementation of Issue #3: User Authentication System for HireIQ.

## ✅ Completed Features

### Backend Implementation

1. **Custom User Model** (`backend/api/models.py`)
   - Email-based authentication (no username)
   - Role-based user types: Candidate, Recruiter, Admin
   - Email verification support
   - User profile with extended information

2. **JWT Authentication** (`backend/hireiq_backend/settings/base.py`)
   - djangorestframework-simplejwt integration
   - Access token lifetime: 60 minutes
   - Refresh token lifetime: 7 days
   - Token rotation enabled for security
   - Blacklist support for revoked tokens

3. **Authentication Endpoints** (`backend/api/views.py`)
   - ✅ User registration with email verification
   - ✅ User login with JWT token generation
   - ✅ User logout with token blacklisting
   - ✅ Email verification
   - ✅ Resend verification email
   - ✅ Password reset request
   - ✅ Password reset confirmation
   - ✅ Password change for authenticated users
   - ✅ User profile management

4. **Serializers** (`backend/api/serializers.py`)
   - UserRegistrationSerializer with password validation
   - UserLoginSerializer
   - PasswordResetRequestSerializer
   - PasswordResetConfirmSerializer
   - PasswordChangeSerializer
   - EmailVerificationSerializer
   - UserSerializer with profile data

5. **Custom Middleware** (`backend/api/middleware.py`)
   - JWTAuthenticationMiddleware - Global JWT auth handling
   - RateLimitMiddleware - IP-based rate limiting
   - SecurityHeadersMiddleware - Security headers for all responses

6. **Custom Permissions** (`backend/api/permissions.py`)
   - IsCandidate - Candidate-only access
   - IsRecruiter - Recruiter-only access
   - IsAdminUser - Admin-only access
   - IsEmailVerified - Verified users only
   - IsCandidateOrRecruiter - Either role can access
   - IsOwnerOrReadOnly - Object-level permissions

7. **Rate Limiting**
   - Login: 5 requests per 5 minutes
   - Registration: 3 requests per hour
   - Password reset: 3 requests per hour
   - Configurable via environment variables

8. **Admin Panel** (`backend/api/admin.py`)
   - Custom UserAdmin with inline profile editing
   - Proper fieldsets for user types
   - Search and filter capabilities

### Frontend Implementation

1. **Authentication Context** (`frontend/src/contexts/AuthContext.jsx`)
   - Centralized auth state management
   - Login/logout functions
   - Token storage in localStorage
   - Axios configuration with auth headers
   - User state persistence

2. **Protected Routes** (`frontend/src/components/auth/ProtectedRoute.jsx`)
   - Route protection based on authentication
   - Role-based route protection
   - Loading states
   - Automatic redirect to login
   - Return URL preservation

3. **Auth Components** (Already exist in `frontend/src/components/auth/`)
   - Login.jsx
   - Register.jsx
   - ForgotPassword.jsx
   - ResetPassword.jsx

4. **Axios Interceptor** (`frontend/src/utils/axios.js`)
   - Automatic token refresh on 401 responses
   - Request interceptor to add auth headers
   - Response interceptor for token rotation
   - Automatic logout on refresh failure

### Security Features

1. **Token Security**
   - JWT tokens with HS256 algorithm
   - Short-lived access tokens (60 min)
   - Refresh token rotation
   - Token blacklisting on logout

2. **Password Security**
   - Django password validation
   - Minimum 8 characters
   - Not too similar to user info
   - Not a common password
   - Cannot be entirely numeric

3. **Rate Limiting**
   - IP-based rate limiting
   - Configurable limits per endpoint
   - Cache-based implementation

4. **Security Headers**
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - X-XSS-Protection: 1; mode=block
   - Referrer-Policy: strict-origin-when-cross-origin

5. **CORS Configuration**
   - Specific origin whitelisting
   - Credentials support for cookies
   - Configurable via environment

---

## 📁 Files Created/Modified

### Backend Files
```
backend/
├── api/
│   ├── models.py                    # ✅ Custom User & UserProfile models
│   ├── serializers.py               # ✅ Auth serializers
│   ├── views.py                     # ✅ Auth views & endpoints
│   ├── urls.py                      # ✅ Auth URL patterns
│   ├── admin.py                     # ✅ Custom admin config
│   ├── middleware.py                # ✅ NEW - Custom middleware
│   └── permissions.py               # ✅ NEW - Role-based permissions
├── hireiq_backend/settings/
│   └── base.py                      # ✅ Updated with JWT & auth settings
├── requirements.txt                 # ✅ Updated with new packages
└── env.example                      # ✅ Updated with auth variables
```

### Frontend Files
```
frontend/
├── src/
│   ├── contexts/
│   │   └── AuthContext.jsx          # ✅ Auth context (already existed)
│   ├── components/auth/
│   │   ├── Login.jsx                # ✅ Login component (already existed)
│   │   ├── Register.jsx             # ✅ Register component (already existed)
│   │   ├── ForgotPassword.jsx       # ✅ Password reset (already existed)
│   │   ├── ResetPassword.jsx        # ✅ Password reset confirm (already existed)
│   │   └── ProtectedRoute.jsx       # ✅ Protected routes (already existed)
│   └── utils/
│       └── axios.js                 # ✅ NEW - Axios config with interceptors
└── .env.example                     # ✅ NEW - Frontend env example
```

### Documentation Files
```
docs/
├── api/
│   └── authentication.md            # ✅ NEW - API documentation
└── development/
    └── AUTHENTICATION_SETUP.md      # ✅ NEW - Setup guide
```

---

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # Edit with your settings
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env  # Edit with your settings
npm run dev
```

---

## 🧪 Testing the Implementation

### 1. Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "user_type": "candidate",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### 3. Test Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/user/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📊 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/register/` | POST | No | Register new user |
| `/api/auth/login/` | POST | No | Login user |
| `/api/auth/logout/` | POST | Yes | Logout user |
| `/api/auth/token/refresh/` | POST | No | Refresh access token |
| `/api/auth/verify-email/<token>/` | GET | No | Verify email |
| `/api/auth/resend-verification/` | POST | No | Resend verification email |
| `/api/auth/password-reset/` | POST | No | Request password reset |
| `/api/auth/password-reset-confirm/` | POST | No | Confirm password reset |
| `/api/auth/password-change/` | POST | Yes | Change password |
| `/api/user/` | GET | Yes | Get current user |
| `/api/user/profile/` | GET/PATCH | Yes | User profile |

---

## 🔑 Environment Variables

### Backend (.env)
```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=hireiq_db
DB_USER=hireiq_user
DB_PASSWORD=hireiq_password
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONTEND_URL=http://localhost:3000
RATELIMIT_ENABLE=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=HireIQ
VITE_APP_ENV=development
```

---

## 📦 New Dependencies Added

### Backend
- `djangorestframework-simplejwt>=5.3,<6.0` - JWT authentication
- `django-ratelimit>=4.1,<5.0` - Rate limiting
- `celery>=5.3,<6.0` - Task queue (for async emails)
- `redis>=5.0,<6.0` - Cache backend

### Frontend
- Already had axios and react-router-dom

---

## ✨ Key Features

### Token Rotation
- New refresh token issued on each refresh
- Old tokens automatically blacklisted
- Prevents token replay attacks

### Role-Based Access
```python
# Example usage in views
from api.permissions import IsRecruiter, IsEmailVerified

class RecruiterOnlyView(APIView):
    permission_classes = [IsRecruiter, IsEmailVerified]
    
    def get(self, request):
        # Only verified recruiters can access
        return Response({'message': 'Welcome, recruiter!'})
```

### Frontend Protected Routes
```jsx
<Route 
  path="/recruiter/dashboard" 
  element={
    <ProtectedRoute requiredUserType="recruiter">
      <RecruiterDashboard />
    </ProtectedRoute>
  } 
/>
```

### Automatic Token Refresh
```javascript
// Axios automatically refreshes tokens on 401
// No manual intervention needed
const response = await axiosInstance.get('/api/protected/');
```

---

## 📝 Acceptance Criteria Status

- ✅ JWT-based authentication
- ✅ User registration with email verification
- ✅ Login/logout functionality
- ✅ Password reset flow
- ✅ Role-based user types (Candidate, Recruiter, Admin)
- ✅ Protected routes on frontend
- ✅ Authentication middleware for API
- ✅ Rate limiting for authentication endpoints
- ✅ Token refresh rotation for security

---

## 🔮 Future Enhancements

1. **Two-Factor Authentication (2FA)**
   - TOTP-based 2FA
   - SMS verification

2. **Social Authentication**
   - Google OAuth
   - LinkedIn OAuth
   - GitHub OAuth

3. **Session Management**
   - View active sessions
   - Revoke specific sessions
   - Device tracking

4. **Advanced Security**
   - IP whitelisting
   - Geolocation-based restrictions
   - Suspicious activity detection

5. **Email Improvements**
   - Async email sending with Celery
   - Email templates with branding
   - Multi-language support

---

## 📚 Documentation

- [API Documentation](docs/api/authentication.md)
- [Setup Guide](docs/development/AUTHENTICATION_SETUP.md)
- [Project Plan](PROJECT_PLAN.md)

---

## 🐛 Known Issues

None at the moment. All acceptance criteria have been met.

---

## 👥 Contributors

- Development Team
- Issue #3 Implementation

---

## 📄 License

[Your License Here]

---

**Status:** ✅ **COMPLETE**  
**Last Updated:** October 2, 2025  
**Version:** 1.0.0 