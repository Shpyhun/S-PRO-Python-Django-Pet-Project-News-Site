from django.urls import path, include
from rest_framework import routers

from .models import News
from .views import NewsView, AddNewsView, NewsDetail, CategoryView, LikeView, CreateCommentViewSet, \
    CategoryAPIView, ProfileUpdate, NewsViewSet, NewsDetailAPIView

router = routers.SimpleRouter()
router.register('api/v1/comments/', CreateCommentViewSet, basename='comments')
router.register('api/v1/news/', NewsViewSet, basename='news')
router.register('api/v1/category/', CategoryAPIView, basename='category')


urlpatterns = [

    path('', NewsView.as_view(), name='news_list'),
    path('news/add_news/', AddNewsView.as_view(), name='add_news'),
    path('news/<slug:news_slug>/', NewsDetail.as_view(), name='news_detail'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('like/<int:pk>/', LikeView.as_view(), name='like_news'),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/profile/', ProfileUpdate.as_view(), name='profile'),
    path('api/v1/news/<int:pk>/', NewsDetailAPIView.as_view(), name='detail-list'),
]
