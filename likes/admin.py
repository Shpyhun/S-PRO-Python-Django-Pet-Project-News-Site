from django.contrib import admin

from likes.models import NewsLikes


@admin.register(NewsLikes)
class NewsLikesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['liked_by', 'news']
    list_display = ['news', 'liked_by', 'like', 'time_create']



