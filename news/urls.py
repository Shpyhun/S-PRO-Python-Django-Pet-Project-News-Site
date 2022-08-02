from django.urls import path
from django.views.decorators.cache import cache_page

from .views import NewsView, news_detail, AddNewsView, view_category

urlpatterns = [
    path('', cache_page(60)(NewsView.as_view()), name='news_list'),
    path('news/add_news/', AddNewsView.as_view(), name='add_news'),
    path('news/<slug:news_slug>/', news_detail, name='news_detail'),
    path('category/<slug:category_slug>/', view_category, name='category'),
]
