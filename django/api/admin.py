from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_email_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_email_verified', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Email verification'), {'fields': ('is_email_verified', 'email_verification_token')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'first_name', 'last_name'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'location', 'experience_years', 'company_name')
    list_filter = ('user__user_type', 'experience_years', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Personal Information'), {
            'fields': ('bio', 'profile_picture', 'date_of_birth', 'location')
        }),
        (_('Candidate Information'), {
            'fields': ('skills', 'experience_years', 'education'),
            'classes': ('collapse',)
        }),
        (_('Recruiter Information'), {
            'fields': ('company_name', 'company_website', 'company_description'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def user_type(self, obj):
        return obj.user.get_user_type_display()
    user_type.short_description = 'User Type'


admin.site.register(User, UserAdmin) 