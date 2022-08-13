from django.contrib import admin

from accounts.forms import RegisterUserForm
from accounts.models import User
from news.models import Comment


class CommentInline(admin.StackedInline):
    model = Comment
    list_display = ['id', 'text']

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_add_permission(self, *args, **kwargs):
        return False


class UserUpdateForm:
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('first_name', 'last_name', 'comments_count')
    search_fields = ['first_name', 'last_name']
    readonly_fields = ['first_name', 'last_name', 'comments_count']
    actions = ["user_activated", "user_deactivated"]

    def comments_count(self, user):
        comments = Comment.objects.filter(user=user)
        comments_count = comments.count()
        return comments_count

    def user_deactivated(self, request, queryset):

        row_update = queryset.update(is_active=False)
        if row_update == '1':
            message_bit = '1 user banned'
        else:
            message_bit = f'{row_update} users banned'
        self.message_user(request, f'{message_bit}')

    def user_activated(self, request, queryset):

        row_update = queryset.update(is_active=True)
        if row_update == '1':
            message_bit = '1 user activated'
        else:
            message_bit = f'{row_update} users activated'
        self.message_user(request, f'{message_bit}')

    user_activated.short_description = 'Activated'
    user_activated.allowed_permissions = ('change',)

    user_deactivated.short_description = 'Deactivated'
    user_deactivated.allowed_permissions = ('change',)







