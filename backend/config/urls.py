from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView

from clients.views import ClientListView
from config.views import health
from trainers.views import TrainerSessionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/health/', health, name='health'),
    path('api/trainer-sessions', TrainerSessionView.as_view(), name='trainer-sessions'),
    path('api/clients', ClientListView.as_view(), name='clients'),
]
