from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with role-based permissions.
    Supports Candidate, Recruiter, and Admin user types.
    """
    
    class UserType(models.TextChoices):
        CANDIDATE = 'candidate', _('Candidate')
        RECRUITER = 'recruiter', _('Recruiter')
        ADMIN = 'admin', _('Admin')
    
    # Override email to be unique and required
    email = models.EmailField(_('email address'), unique=True)
    
    # User type field
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CANDIDATE,
        verbose_name=_('user type')
    )
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    # Override username to use email
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    
    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    @property
    def is_candidate(self):
        return self.user_type == self.UserType.CANDIDATE
    
    @property
    def is_recruiter(self):
        return self.user_type == self.UserType.RECRUITER
    
    @property
    def is_admin(self):
        return self.user_type == self.UserType.ADMIN


class UserProfile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Common fields
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Candidate-specific fields
    skills = models.JSONField(default=list, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.JSONField(default=list, blank=True)
    
    # Recruiter-specific fields
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"{self.user.email} - Profile" 