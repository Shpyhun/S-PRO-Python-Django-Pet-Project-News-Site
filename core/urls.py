from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from news.urls import router
from news.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),

    # path('', include(router.urls), name='comments'),
    path('', include(router.urls), name='news'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
