from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, StudentSerializer, MentorStudentSerializer, BhaagSerializer, SessionSerializer, VideoBhaagSerializer, AttendanceSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action 
from django.contrib.auth import authenticate
from .models import Student, Mentor, Parent, Volunteer, VideoBhaag, Attendance, Session, Bhaag, BhaagClassSection, ResourceBhaag
from datetime import date
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db.models import Count


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

    def delete(self, request):
        try:
            user=User.objects.get(username=request.GET.get('username'))
            user.is_active=False
            user.save()
            response={
                "status": "success",
                "message": "Delete successful",
                "data": ""
            }
            return Response(response)
        except Exception as e:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "401",
                        "message": "account delete failed",
                        "details": "Please Try again."
                    }
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        try:
            response = super().post(request, *args, **kwargs)
            
            # Customize the response data as needed
            if response.status_code == status.HTTP_200_OK:
                response={
                    "status": "success",
                    "message": "refresh successful",
                    "data": {'access_token': response.data.get('access'), 'refresh_token': response.data.get('refresh')},
                }
                return Response(response)
            else:
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Bad Request",
                        "details": "Refresh Token Failed"
                    }
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Refresh Token Failed",
                        "details": f"{e}"
                    }
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TokenVerifyAPIView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == status.HTTP_200_OK:
                response={
                    "status": "success",
                    "message": "verification successful",
                    "data": {}
                }
                return Response(response)
            else:
                response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Bad Request",
                        "details": "Verify Token Failed"
                    }
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response={
                "status": "error",
                "message": "",
                "data": {},
                "error": {
                    "code": "400",
                    "message": "Bad Request",
                    "details": f"Verify Token Failed, {e}"
                }
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
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
        try:
            from .models import UserProfile
            request_data=request.data
            if user_profile_id:=int(request_data.get("user_profile_id")):
                serializer = UserSerializer(UserProfile.objects.get(id=user_profile_id).user, data=request_data, partial=True)
            else:
                serializer = UserSerializer(request.user, data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response={
                    "status": "success",
                    "message": "profile updated successful",
                    "data": serializer.data
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
                        "details": serializer.errors
                    }
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response={
                    "status": "error",
                    "message": "",
                    "data": {},
                    "error": {
                        "code": "400",
                        "message": "Bad Request",
                        "details": e
                    }
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


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
                session_objects_online = Session.objects.filter(date=session_date, bhaag_class_section__bhaag_class__bhaag_category__category="online")
                session_objects_offline = Session.objects.filter(date=session_date, bhaag_class_section__bhaag_class__bhaag_category__category="offline")
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
        try:
            from .models import Session
            session=Session.objects.get(id=request.data.get('session_id'))
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
        try:
            from .models import BhaagClass, BhaagCategory, Bhaag, Location, BhaagClassSection
            if bhaag_class_section_id:=request.GET.get('bhaag_class_section_id'):
                bhaag_class_section=BhaagClassSection.objects.get(id=bhaag_class_section_id)
            # elif bhaag_class_id:=request.GET.get('bhaag_class_id'):
            #     bhaag_class=BhaagClass.objects.get(id=bhaag_class_id)
            # elif request.GET.get('bhaag_id') or request.GET.get('bhaag_category') or request.GET.get('location_id'):
            #     bhaag_class=BhaagClass.objects.get(
            #         category=BhaagCategory.objects.get(
            #             bhaag=Bhaag.objects.get(id=request.GET.get('bhaag_id')),
            #             category=request.GET.get('bhaag_category'),
            #         ),
            #         location=Location.objects.get(id=request.GET.get('location_id'))
            #     )
            # else:
            #     mentor=Mentor.objects.get(profile=request.user.profile)
            #     students=Student.objects.filter(bhaag_class=mentor.bhaag_class)
            students=Student.objects.filter(bhaag_class_section=bhaag_class_section)
            serializer = MentorStudentSerializer(students, many=True)
            response={
                "status": "success",
                "message": "students fetch successful",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
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



class AttendanceReportAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Retrieve student ID from the request

            student_id = int(request.GET.get('student_id')) if request.GET.get('student_id') else None
            bhaag_id = int(request.GET.get('bhaag_id')) if request.GET.get('bhaag_id') else None
            bhaag_class_section_id = int(request.GET.get('bhaag_class_section_id')) if request.GET.get('bhaag_class_section_id') else None

            attendance_report = {}
            # Get student's attendance reports

            total_sessions_ytd = Session.objects.filter(
                date__gte=date.today().replace(month=1, day=1),
                date__lte=date.today()
            ).values('date').annotate(count=Count('date')).count() #.count() #TODO COUNT SHOULD BE OF SESSION OF SPECIFIC BHAAG 
            total_sessions_mtd = Session.objects.filter(
                date__gte=date.today().replace(day=1),
                date__lte=date.today()
            ).values('date').annotate(count=Count('date')).count() #.count() #TODO COUNT SHOULD BE OF SESSION OF SPECIFIC BHAAG 


            if student_id: #STUDENT's OWN ATTENDANCE
                student = Student.objects.get(id=student_id)
                student_attendance = Attendance.objects.filter(student=student)

                # Calculate student's attendance percentage and count YTD, MTD
                student_attendance_ytd = student_attendance.filter(
                    session__date__gte=date.today().replace(month=1, day=1),
                    session__date__lte=date.today()
                ).count()
                student_attendance_mtd = student_attendance.filter(
                    session__date__gte=date.today().replace(day=1),
                    session__date__lte=date.today()
                ).count()

                student_attendance_percentage_ytd = (
                    student_attendance_ytd / total_sessions_ytd
                ) * 100 if total_sessions_ytd > 0 else 0

                student_attendance_percentage_mtd = (
                    student_attendance_mtd / total_sessions_mtd
                ) * 100 if total_sessions_mtd > 0 else 0

                student_report = {
                    'attendance_percentage_ytd': student_attendance_percentage_ytd,
                    'attendance_count_ytd': student_attendance_ytd,
                    'attendance_percentage_mtd': student_attendance_percentage_mtd,
                    'attendance_count_mtd': student_attendance_mtd,
                }
                attendance_report.update(student_report)

            if bhaag_class_section_id: #OVERALL CLASS ATTENDANCE, (for Mentor/Bhag Owners) 
                # Calculate overall attendance for BhaagClassSection YTD, MTD
                bhaag_class_section_attendance_ytd = Attendance.objects.filter(
                    session__date__gte=date.today().replace(month=1, day=1),
                    session__date__lte=date.today(),
                    session__bhaag_class_section=bhaag_class_section_id
                ).count()

                bhaag_class_section_attendance_mtd = Attendance.objects.filter(
                    session__date__gte=date.today().replace(day=1),
                    session__date__lte=date.today(),
                    session__bhaag_class_section=bhaag_class_section_id
                ).count()

                if student_id==0:
                    for student in Student.objects.filter(bhaag_class_section_id=bhaag_class_section_id):
                        # student = Student.objects.get(id=student_id)
                        student_attendance = Attendance.objects.filter(student_id=student)

                        # Calculate student's attendance percentage and count YTD, MTD
                        student_attendance_ytd = student_attendance.filter(
                            session__date__gte=date.today().replace(month=1, day=1),
                            session__date__lte=date.today()
                        ).count()
                        student_attendance_mtd = student_attendance.filter(
                            session__date__gte=date.today().replace(day=1),
                            session__date__lte=date.today()
                        ).count()

                        student_attendance_percentage_ytd = (
                            student_attendance_ytd / total_sessions_ytd
                        ) * 100 if total_sessions_ytd > 0 else 0

                        student_attendance_percentage_mtd = (
                            student_attendance_mtd / total_sessions_mtd
                        ) * 100 if total_sessions_mtd > 0 else 0

                        student_report = {
                            'attendance_percentage_ytd': student_attendance_percentage_ytd,
                            'attendance_count_ytd': student_attendance_ytd,
                            'attendance_percentage_mtd': student_attendance_percentage_mtd,
                            'attendance_count_mtd': student_attendance_mtd,
                        }
                        attendance_report.update({student.profile.first_name:student_report})
                else:
                    bhaag_class_section_report = {
                        'bhaag_class_section_attendance_percentage_ytd': (
                            bhaag_class_section_attendance_ytd / total_sessions_ytd
                        ) * 100 if total_sessions_ytd > 0 else 0,
                        'bhaag_class_section_attendance_count_ytd': bhaag_class_section_attendance_ytd,
                        'bhaag_class_section_attendance_percentage_mtd': (
                            bhaag_class_section_attendance_mtd / total_sessions_mtd
                        ) * 100 if total_sessions_mtd > 0 else 0,
                        'bhaag_class_section_attendance_count_mtd': bhaag_class_section_attendance_mtd,
                    }
                    attendance_report.update(bhaag_class_section_report)
            elif bhaag_class_section_id==0:
                attendance_report.update({"offline":{}})
                attendance_report.update({"online":{}})
                for bhaag_class_section in BhaagClassSection.objects.all():
                    bhaag_class_section_id = bhaag_class_section
                    bhaag_class_section_attendance_ytd = Attendance.objects.filter(
                        session__date__gte=date.today().replace(month=1, day=1),
                        session__date__lte=date.today(),
                        session__bhaag_class_section=bhaag_class_section_id
                    ).count()

                    bhaag_class_section_attendance_mtd = Attendance.objects.filter(
                        session__date__gte=date.today().replace(day=1),
                        session__date__lte=date.today(),
                        session__bhaag_class_section=bhaag_class_section_id
                    ).count()

                                
                    bhaag_class_section_report = {
                        'bhaag_class_section_attendance_percentage_ytd': (
                            bhaag_class_section_attendance_ytd / total_sessions_ytd
                        ) * 100 if total_sessions_ytd > 0 else 0,
                        'bhaag_class_section_attendance_count_ytd': bhaag_class_section_attendance_ytd,
                        'bhaag_class_section_attendance_percentage_mtd': (
                            bhaag_class_section_attendance_mtd / total_sessions_mtd
                        ) * 100 if total_sessions_mtd > 0 else 0,
                        'bhaag_class_section_attendance_count_mtd': bhaag_class_section_attendance_mtd,
                    }
                    attendance_report[bhaag_class_section.bhaag_class.bhaag_category.category].update({f"{bhaag_class_section.bhaag_class.bhaag_category.bhaag.name}-{bhaag_class_section.section}":bhaag_class_section_report})


            if bhaag_id:
                # Calculate overall attendance for BhaagClassSection YTD, MTD
                bhaag_attendance_ytd = Attendance.objects.filter(
                    session__date__gte=date.today().replace(month=1, day=1),
                    session__date__lte=date.today(),
                    session__bhaag_class_section__bhaag_class__bhaag_category__bhaag_id=bhaag_id
                ).count()

                bhaag_attendance_mtd = Attendance.objects.filter(
                    session__date__gte=date.today().replace(day=1),
                    session__date__lte=date.today(),
                    session__bhaag_class_section__bhaag_class__bhaag_category__bhaag_id=bhaag_id
                ).count()

                bhaag_report = {
                    'bhaag_attendance_percentage_ytd': (
                        bhaag_attendance_ytd / total_sessions_ytd
                    ) * 100 if total_sessions_ytd > 0 else 0,
                    'bhaag_attendance_count_ytd': bhaag_attendance_ytd,
                    'bhaag_attendance_percentage_mtd': (
                        bhaag_attendance_mtd / total_sessions_mtd
                    ) * 100 if total_sessions_mtd > 0 else 0,
                    'bhaag_attendance_count_mtd': bhaag_attendance_mtd,
                }
                attendance_report.update(bhaag_report)
            elif bhaag_id==0:
                for bhaag in Bhaag.objects.all():
                    bhaag_id = bhaag
                    bhaag_attendance_ytd = Attendance.objects.filter(
                        session__date__gte=date.today().replace(month=1, day=1),
                        session__date__lte=date.today(),
                        session__bhaag_class_section__bhaag_class__bhaag_category__bhaag_id=bhaag_id
                    ).count()

                    bhaag_attendance_mtd = Attendance.objects.filter(
                        session__date__gte=date.today().replace(day=1),
                        session__date__lte=date.today(),
                        session__bhaag_class_section__bhaag_class__bhaag_category__bhaag_id=bhaag_id
                    ).count()

                    bhaag_report = {
                        'bhaag_attendance_percentage_ytd': (
                            bhaag_attendance_ytd / total_sessions_ytd
                        ) * 100 if total_sessions_ytd > 0 else 0,
                        'bhaag_attendance_count_ytd': bhaag_attendance_ytd,
                        'bhaag_attendance_percentage_mtd': (
                            bhaag_attendance_mtd / total_sessions_mtd
                        ) * 100 if total_sessions_mtd > 0 else 0,
                        'bhaag_attendance_count_mtd': bhaag_attendance_mtd,
                    }
                    attendance_report.update({bhaag.name:bhaag_report})

            response={
                "status": "success",
                "message": "attendance reports generated successfully",
                "data": attendance_report,
            }
            return Response(response)
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
            return Response(response)
        

# class AttendanceReportAPIView(APIView):

# class LocationAPIView(APIView):



class ResourceBhaagAutocompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query_param = request.query_params.get('title', '')
            results = self.get_autocomplete_results(query_param)
            response={
                "status": "success",
                "message": "attendance reports generated successfully",
                "data": results,
            }
            return Response(response, status=status.HTTP_200_OK)
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
            return Response(response)

    def get_autocomplete_results(self, query_param):
        queryset = ResourceBhaag.objects.filter(
            Q(title__icontains=query_param)
        )

        results = [{'id': item.id, 'title': item.title} for item in queryset]

        return results


# from rest_framework import generics
