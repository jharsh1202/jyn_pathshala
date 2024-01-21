from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ProfileAPIView, StudentsAPIView, RoleProfileAPIView, \
    BhaagListView, SessionAPIView, AttendanceAPIView, LogoutAPIView, RefreshAPIView, TokenVerifyAPIView, \
        VideoLibraryAPIView, AttendanceReportAPIView, ResourceBhaagAutocompleteView, ResourceBhaagAPIView 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', RefreshAPIView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyAPIView.as_view(), name='token_verify'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='login'),
    path('bhaag/', BhaagListView.as_view(), name='bhaag'),
    path('session/', SessionAPIView.as_view(), name='session'),
    path('attendance/', AttendanceAPIView.as_view(), name='attendance'),
    path('attendance_report/', AttendanceReportAPIView.as_view(), name='attendance_report'),
    path('students/', StudentsAPIView.as_view(), name='student'),
    # path('role_profile/', RoleProfileAPIView.as_view(), name='role_profile'),
    path('resources/', ResourceBhaagAutocompleteView.as_view(), name='resources'),
    path('resource/', ResourceBhaagAPIView.as_view(), name='resource'),
    path('video_library/', VideoLibraryAPIView.as_view(), name='video_library'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)