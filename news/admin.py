from django.contrib import admin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from news.models import News, Category, Comment


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo', 'content', 'category',
                    'slug', 'is_published', 'likes_count', 'comments_count')
    search_fields = ['title', ]
    list_filter = ['category', ]
    list_editable = ['slug', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['preview', 'likes_count', 'comments_count']

    def preview(self, object):
        return mark_safe(f"<img src='{object.photo.url}'")

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=60>")

    get_html_photo.short_description = "Photo"

    def comments_count(self, news):
        comments = Comment.objects.filter(news=news)
        comments_count = comments.count()
        return comments_count

    # def get_comments_count(self, object):
    #     pass
    #
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         _comment_count=Count("comment", distinct=True),
    #     )
    #     return queryset

    # def comment_count(self, obj):
    #     return obj.comment_set.count()

    # def comment_count(self, obj):
    #     return obj._comment_count

    # comment_count.admin_order_field = '_comment_count'


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'text', 'news', 'user')
#     search_fields = ['text', 'news']
#     list_filter = ['text', 'news']

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         _text_count=Count("t", distinct=True),
    #         _villain_count=Count("villain", distinct=True),
    #     )
    #     return queryset

    # def comment_count(self, obj):
    #     return obj.comment_set.count()

    # def has_delete_permission(self, *args, **kwargs):
    #     return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_editable = ['name', ]
    prepopulated_fields = {'slug': ('name',)}






