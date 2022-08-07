from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name', 'email']


# @admin.register(User)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'email', 'user', 'first_name', 'last_name']
#     search_fields = ['first_name', 'last_name', 'email']
