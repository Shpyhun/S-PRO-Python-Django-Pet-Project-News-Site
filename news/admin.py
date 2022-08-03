from django.contrib import admin
from django.utils.safestring import mark_safe

from news.models import News, Comment, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_html_photo', 'content', 'category', 'slug', 'is_published']
    search_fields = ['title', ]
    list_filter = ['category', ]
    list_editable = ['slug', 'is_published']
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = News

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=60>")

    get_html_photo.short_description = "Photo"


admin.site.register(News, NewsAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'news', 'user']
    search_fields = ['text', 'news']
    list_filter = ['text', 'news']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_editable = ['name', ]
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)



