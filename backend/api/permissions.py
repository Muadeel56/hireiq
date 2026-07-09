"""
Custom permissions for role-based access control
"""
from rest_framework import permissions


class IsCandidate(permissions.BasePermission):
    """
    Permission to only allow candidates to access a view.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_candidate


class IsRecruiter(permissions.BasePermission):
    """
    Permission to only allow recruiters to access a view.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_recruiter


class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access a view.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsEmailVerified(permissions.BasePermission):
    """
    Permission to only allow users with verified emails to access a view.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_email_verified


class IsCandidateOrRecruiter(permissions.BasePermission):
    """
    Permission to allow both candidates and recruiters to access a view.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_candidate or request.user.is_recruiter)
        )
