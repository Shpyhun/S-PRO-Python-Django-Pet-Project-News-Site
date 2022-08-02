from django.contrib import admin

from news.models import Profile, News, Comment, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'photo', 'category', 'slug', 'is_published']
    search_fields = ['title', ]
    list_filter = ['category', ]
    list_editable = ['content', 'slug', 'is_published']
    prepopulated_fields = {'slug': ('title',)}

    class Meta:
        model = News


admin.site.register(News, NewsAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'news', 'user']
    search_fields = ['id', 'text', 'news']
    list_filter = ['id', 'text', 'news']
    list_editable = ['text', ]

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', ]
    search_fields = ['first_name', 'last_name']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_editable = ['name', ]
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)



