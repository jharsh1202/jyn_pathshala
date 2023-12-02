from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ProfileAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)