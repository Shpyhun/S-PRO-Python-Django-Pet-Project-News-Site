from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from news.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('likes/', include('likes.urls')),
    path('weather/', include('weather.urls')),
    # path('weather/', include('weather.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
