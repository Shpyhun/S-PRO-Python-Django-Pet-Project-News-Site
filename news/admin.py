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

    def likes_count(self):
        return self.likes.count()

    def comments_count(self, news):
        comments = Comment.objects.filter(news=news)
        comments_count = comments.count()
        return comments_count


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_editable = ['name', ]
    prepopulated_fields = {'slug': ('name',)}






