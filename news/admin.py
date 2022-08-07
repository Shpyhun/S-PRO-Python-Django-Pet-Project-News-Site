from django.contrib import admin
from django.utils.safestring import mark_safe

from news.models import News, Comment, Category


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_html_photo', 'content', 'category', 'slug', 'is_published']
    search_fields = ['title', ]
    list_filter = ['category', ]
    list_editable = ['slug', 'is_published']
    prepopulated_fields = {'slug': ('title',)}

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=60>")

    get_html_photo.short_description = "Photo"
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'get_html_photo', 'content', 'category', 'slug', 'is_published']
#     search_fields = ['title', ]
#     list_filter = ['category', ]
#     list_editable = ['slug', 'is_published']
#     prepopulated_fields = {'slug': ('title',)}
#
#     class Meta:
#         model = News


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'news', 'user']
    search_fields = ['text', 'news']
    list_filter = ['text', 'news']

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'text', 'news', 'user']
#     search_fields = ['text', 'news']
#     list_filter = ['text', 'news']
#
#     class Meta:
#         model = Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_editable = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'slug']
#     list_editable = ['name', ]
#     prepopulated_fields = {'slug': ('name',)}
#
#     class Meta:
#         model = Category
#
#
# admin.site.register(News, NewsAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Category, CategoryAdmin)



