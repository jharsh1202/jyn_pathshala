from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, StudentSerializer, MentorStudentSerializer, BhaagSerializer, SessionSerializer, VideoBhaagSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action 
from django.contrib.auth import authenticate
from .models import Student, Mentor, Parent, Volunteer, VideoBhaag
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class VideoLibraryPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 50


class RegistrationAPIView(APIView): 
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                "status": "success",
                "message": "Registration successful",
                "data": {},
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response={
                "status": "error",
                "message": "",
                "data": {},
                "error": {
                    "code": "400",
                    "message": "Bad Request",
                    "details": serializer.errors
                }
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            # Customize the response data as needed
            if response.status_code == status.HTTP_200_OK:
                response={
                    "status": "success",
                    "message": "Login successful",
                    "data": {'access_token': response.data.get('access'), 'refresh_token': response.data.get('refresh')},
                }
                return Response(response)
            else:
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "401",
                        "message": "Invalid credentials",
                        "details": "Please Try again."
                    }
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "401",
                        "message": "Invalid credentials",
                        "details": "Please Try again."
                    }
                }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

class RefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Customize the response data as needed
        if response.status_code == status.HTTP_200_OK:
            response={
                "status": "success",
                "message": "refresh successful",
                "data": {'access_token': response.data.get('access'), 'refresh_token': response.data.get('refresh')},
            }
            return Response(response)
        

class TokenVerifyAPIView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Customize the response data as needed
        if response.status_code == status.HTTP_200_OK:
            response={
                "status": "success",
                "message": "verification successful",
                "data": {}
            }
        return Response(response)


# class LoginAPIView(APIView):


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                raise ValueError("Refresh token is required for logout.")

            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response_data = {
                "status": "success",
                "message": "Logout successful",
                "data": {},
            }

            return Response(response_data)

        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Unexpected Error",
                "data": {},
                "error": {
                    "code": "500",
                    "message": str(e),
                    "details": str(e),
                }
            }

            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        response={
            "status": "success",
            "message": "profile fetch successful",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    

    def patch(self, request, format=None):
        from .models import UserProfile
        request_data=request.data
        if user_profile_id:=int(request_data.get("user_profile_id")):
            serializer = UserSerializer(UserProfile.objects.get(id=user_profile_id).user, data=request_data, partial=True)
        else:
            serializer = UserSerializer(request.user, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BhaagListView(APIView):
    def get(self, request, *args, **kwargs):
        from .models import Bhaag
        if request.GET.get('bhaag_id'):
            bhaag_objects = Bhaag.objects.get(id=request.GET.get('bhaag_id'))
            serializer = BhaagSerializer(bhaag_objects)
        else:
            bhaag_objects = Bhaag.objects.all()
            serializer = BhaagSerializer(bhaag_objects, many=True)

        response={
            "status": "success",
            "message": "Bhaag fetch successful",
            "data": serializer.data 
        }
        return Response(response, status=status.HTTP_200_OK)
    

class SessionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            from .models import Session
            
            if session_date:=request.GET.get('date'):
                session_objects_online = Session.objects.filter(date=session_date, bhaag_class_section__bhaag_class__bhaag_category__category="online", is_active=True)
                session_objects_offline = Session.objects.filter(date=session_date, bhaag_class_section__bhaag_class__bhaag_category__category="offline", is_active=True)
            else:
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Bad Request",
                        "details": "date not found"
                    }
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            serializer_online = SessionSerializer(session_objects_online, many=True)
            serializer_offline = SessionSerializer(session_objects_offline, many=True)

            response={
                "status": "success",
                "message": "Session fetch successful",
                "data": {
                    "online":serializer_online.data, 
                    "offline": serializer_offline.data
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Unexpected Error",
                        "details": f"{e}"
                    }
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        from .models import Session
        session=Session.objects.get(id=request.data.get('session_id'))
        print(request.data)
        session_serializer=SessionSerializer(session, data=request.data, partial=True)
        if session_serializer.is_valid():
            session_serializer.save()
            response={
                "status": "success",
                "message": "Session update successful",
                "data": ""
            }
            return Response(response)
        else:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Unexpected Error",
                        "details": f"{session_serializer.errors}"
                    }
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)




class RoleProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        data=request.data
        user_profile=user.profile

        if user_profile.role == 'Student':
            student=Student.objects.create(profile=user_profile)
            student.bhaag_class_id = data.get('bhaag_class') 
            student.save() 
        if user_profile.role == 'Mentor':
            from .models import BhaagClass, BhaagCategory, Location
            bhaag_class=BhaagClass.objects.get(bhaag_category=BhaagCategory.objects.get(bhaag_id=data.get('bhaag_id'), category=data.get('bhaag_category')), location=Location.objects.get(id=data.get('location_id')))
            mentor=Mentor.objects.create(profile=user_profile, bhaag_class=bhaag_class) #TODO
            mentor.save()
        response={
            "status": "success",
            "message": "profile created successful",
            "data": {},
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .models import BhaagClass, BhaagCategory, Bhaag, Location, BhaagClassSection
        if bhaag_class_section_id:=request.GET.get('bhaag_class_section_id'):
            bhaag_class_section=BhaagClassSection.objects.get(id=bhaag_class_section_id)
        students=Student.objects.filter(bhaag_class_section=bhaag_class_section)
        serializer = MentorStudentSerializer(students, many=True)
        response={
            "status": "success",
            "message": "students fetch successful",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class AttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            from .models import BhaagClass, BhaagCategory, Bhaag, Location, BhaagClassSection, Attendance, Session
            if bhaag_class_section_id:=request.GET.get('bhaag_class_section_id'):
                date=request.GET.get('date') 
                try:
                    session=Session.objects.get(bhaag_class_section_id=bhaag_class_section_id, date=date)
                except Session.DoesNotExist:
                    raise ValueError("Session not found")
                attendance_record=Attendance.objects.filter(session=session, status=True).values_list('student_id', flat=True)
                response={
                    "status": "success",
                    "message": "attendance records fetch successful",
                    "data": attendance_record
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response={
                        "status": "error",
                        "message": "",
                        "data": {},
                        "error": {
                            "code": "400",
                            "message": "Bad Request",
                            "details": "bhaag_class_section_id",
                        }
                    }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response={
                        "status": "error",
                        "message": "",
                        "data": {},
                        "error": {
                            "code": "500",
                            "message": "Unexpected Error",
                            "details": f"{e}",
                        }
                    }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            from .models import Session, Attendance
            request_data = request.data
            student_ids=request_data.get('students_ids', [])
            students=Student.objects.filter(id__in=student_ids)
            session=Session.objects.get(id=request_data.get('session_id'))
            
            if students.count()!=len(student_ids):
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "404",
                        "message": "failed to fetch some students",
                        "details": f"{students} {session}",
                    }
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            if not students or not session:
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Bad Request",
                        "details": f"{students} {session}",
                    }
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    for student in students:
                        Attendance.objects.update_or_create(student=student, session=session, status=True)
                response={
                    "status": "success",
                    "message": "attendance marked successfully",
                    "data": "",
                }
                return Response(response)
            except Exception as e:
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Bad Request",
                        "details": str(e),
                    }
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "500",
                        "message": "Unexpected Error",
                        "details": str(e),
                    }
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VideoLibraryAPIView(APIView):
    pagination_class = VideoLibraryPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            bhaag_id = request.GET.get('bhaag_id')
            category = request.GET.get('category')
            search = request.GET.get('search')

            # Build Q objects for dynamic filtering
            filters = Q()

            if bhaag_id:
                filters &= Q(bhaag__id=bhaag_id)

            if category:
                filters &= Q(category=category)

            if search:
                filters &= Q(title__icontains=search)

            # Filter queryset based on parameters
            queryset = VideoBhaag.objects.filter(filters)

            # Apply pagination
            paginator = VideoLibraryPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize the paginated queryset
            serializer = VideoBhaagSerializer(paginated_queryset, many=True)

            # Return the serialized data in the response
            paginated_response = paginator.get_paginated_response(serializer.data)
            response={
                "status": "success",
                "message": "video library records fetch successful",
                "data": paginated_response.data
            }
            return Response(response)
        except Exception as e:
            response={
                "status": "error",
                "message": "",
                "data": {},
                "error": {
                    "code": "400",
                    "message": "Bad Request",
                    "details": str(e),
                }
            }
            return Response(response)


# class LocationAPIView(APIView):
