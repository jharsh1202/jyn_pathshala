from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ProfileAPIView


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='login'),
]