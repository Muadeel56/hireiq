import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Configure axios defaults
  axios.defaults.baseURL = 'http://localhost:8000/api';
  axios.defaults.headers.common['Content-Type'] = 'application/json';

  // Add token to requests if available
  const token = localStorage.getItem('access_token');
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const response = await axios.get('/user/');
          setUser(response.data);
        } catch (error) {
          console.error('Auth check failed:', error);
          logout();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await axios.post('/auth/login/', {
        email,
        password,
      });

      const { tokens, user: userData } = response.data;
      
      // Store tokens
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      
      // Set authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`;
      
      setUser(userData);
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      const response = await axios.post('/auth/register/', userData);
      
      setUser(response.data.user);
      return { success: true, message: response.data.message };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Registration failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    // Clear tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Clear authorization header
    delete axios.defaults.headers.common['Authorization'];
    
    setUser(null);
    setError(null);
  };

  const updateProfile = async (profileData) => {
    try {
      setError(null);
      const response = await axios.patch('/user/profile/', profileData);
      setUser({ ...user, profile: response.data });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Profile update failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const changePassword = async (oldPassword, newPassword, newPasswordConfirm) => {
    try {
      setError(null);
      await axios.post('/auth/password-change/', {
        old_password: oldPassword,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm,
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Password change failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const requestPasswordReset = async (email) => {
    try {
      setError(null);
      await axios.post('/auth/password-reset/', { email });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Password reset request failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const resetPassword = async (token, newPassword, newPasswordConfirm) => {
    try {
      setError(null);
      await axios.post('/auth/password-reset-confirm/', {
        token,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm,
      });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Password reset failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const resendVerification = async (email) => {
    try {
      setError(null);
      await axios.post('/auth/resend-verification/', { email });
      return { success: true };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Verification email send failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    requestPasswordReset,
    resetPassword,
    resendVerification,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 