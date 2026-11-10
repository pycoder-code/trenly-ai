from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView

from config.views import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/health/', health, name='health'),
]
