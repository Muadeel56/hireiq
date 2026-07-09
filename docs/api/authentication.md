# Authentication API Documentation

## Overview
HireIQ uses JWT (JSON Web Token) based authentication with token rotation for enhanced security.

## Authentication Endpoints

### 1. User Registration
**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "user_type": "candidate",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully. Please check your email for verification.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "candidate",
    "is_email_verified": false
  }
}
```

**Rate Limit:** 3 requests per hour per IP

---

### 2. User Login
**POST** `/api/auth/login/`

Authenticate a user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "candidate",
    "is_email_verified": true
  }
}
```

**Rate Limit:** 5 requests per 5 minutes per IP

---

### 3. Token Refresh
**POST** `/api/auth/token/refresh/`

Refresh an expired access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Security Features

### JWT Token Rotation
- Refresh tokens are rotated on each use
- Old refresh tokens are blacklisted
- Access token lifetime: 60 minutes
- Refresh token lifetime: 7 days

### Rate Limiting
- Login: 5 attempts per 5 minutes
- Registration: 3 attempts per hour
- Password Reset: 3 attempts per hour

### Role-Based Access Control
- **Candidate**: Can apply for jobs, manage profile
- **Recruiter**: Can post jobs, review applications
- **Admin**: Full system access

---

## Frontend Integration Example

```javascript
// Using axios interceptor for automatic token refresh
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',
});

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      const { data } = await axios.post('/auth/token/refresh/', {
        refresh: refreshToken
      });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      return axiosInstance(error.config);
    }
    return Promise.reject(error);
  }
);
``` 