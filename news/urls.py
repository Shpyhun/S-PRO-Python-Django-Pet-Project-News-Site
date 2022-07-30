from django.urls import path

from .views import NewsView, news_list_sorted, news_detail, AddNewsView, view_category

urlpatterns = [
    path('', NewsView.as_view(), name='news_list'),
    path('news/sorted/<int:index>/', news_list_sorted, name='sorted'),

    path('news/<int:index>/', news_detail, name='news_detail'),
    path('news/add_news/', AddNewsView.as_view(), name='add_news'),
    path('category/<int:category_id>/', view_category, name='category'),
]
