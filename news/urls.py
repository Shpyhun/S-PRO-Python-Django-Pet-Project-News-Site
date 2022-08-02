from django.urls import path

from .views import NewsView, news_detail, AddNewsView, view_category

urlpatterns = [
    path('', NewsView.as_view(), name='news_list'),
    path('news/<slug:news_slug>/', news_detail, name='news_detail'),
    path('news/add_news/', AddNewsView.as_view(), name='add_news'),
    path('category/<slug:category_slug>/', view_category, name='category'),
]
