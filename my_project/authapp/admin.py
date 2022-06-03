from django.contrib import admin

from settingsapp.admin import BaseAdminSettings
from authapp import models

# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    list_per_page: int = 10
    search_fields = ['username', 'first_name', 'last_name', 'email']
    