from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Making password field non-editable
    fieldsets = []
    filter_horizontal = []
    list_filter = []

    # changing the display menu of User model at admin panel
    list_display = ['email', 'first_name', 'last_name', 'username', 'role', 'is_active']

    # ordering the list of users depending on the date_joined field descending
    ordering = ['-date_joined']
    


admin.site.register(User, CustomUserAdmin)

admin.site.register(UserProfile)
