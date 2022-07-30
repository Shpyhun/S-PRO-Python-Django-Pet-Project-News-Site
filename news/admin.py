from django.contrib import admin

from news.models import Profile, News, CommentNews

admin.site.register(Profile)


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'photo', 'category', 'is_published']
    search_fields = ['title', ]
    list_filter = ['category', ]
    list_editable = ['title', ]

    class Meta:
        model = News


admin.site.register(News, NewsAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'news', 'user']
    search_fields = ['id', 'text', 'news']
    list_filter = ['id', 'text', 'news']
    list_editable = ['text']

    class Meta:
        model = CommentNews


admin.site.register(CommentNews, CommentAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', ]
    search_fields = ['first_name', 'last_name', ]



