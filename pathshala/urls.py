from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ProfileAPIView, StudentsAPIView, RoleProfileAPIView, BhaagListView, SessionAPIView, AttendanceAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='login'),
    path('bhaag/', BhaagListView.as_view(), name='bhaag'),
    path('session/', SessionAPIView.as_view(), name='session'),
    path('attendance/', AttendanceAPIView.as_view(), name='session'),
    path('students/', StudentsAPIView.as_view(), name='student'),
    path('role_profile/', RoleProfileAPIView.as_view(), name='student'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)