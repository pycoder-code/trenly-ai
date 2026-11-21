"""Корневые пути: админка, схема, здоровье и API доменов."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

from config.views import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/health/', health, name='health'),
    path('api/', include('trainers.api.urls')),
    path('api/', include('clients.api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.TRAINER_PHOTO_URL, document_root=settings.TRAINER_PHOTO_ROOT)
