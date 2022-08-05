from django.urls import path

from .views import NewsView, AddNewsView, NewsDetail, CategoryView

urlpatterns = [
    # path('', cache_page(60)(NewsView.as_view()), name='news_list'),
    path('', NewsView.as_view(), name='news_list'),
    path('news/add_news/', AddNewsView.as_view(), name='add_news'),
    path('news/<slug:news_slug>/', NewsDetail.as_view(), name='news_detail'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    # path('category/<slug:category_slug>/', view_category, name='category'),
]
