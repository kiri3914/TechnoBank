from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 
                    'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
    
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 
                       'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 
                       'password1', 'password2')
        }),
    )