from django.contrib import admin

from accounts.models import User
from news.models import Comment


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['id', 'email', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name']



