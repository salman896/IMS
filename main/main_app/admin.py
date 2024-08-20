from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    # Define which fields to display in the admin interface
    list_display = ('username', 'is_staff')

    # Define which fields are editable in the admin interface
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','is_approved', 'role')}),
    )

    # Define fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'role'),
        }),
    )



# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Add_job)

admin.site.register(Add_profile)

admin.site.register(com_profile)

admin.site.register(Applay_job)



