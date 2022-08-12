from django.contrib import admin

from accounts.models import User
from news.models import Comment


class CommentInline(admin.StackedInline):
    model = Comment
    list_display = ['id', 'text']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    readonly_fields = ['first_name', 'last_name']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False




