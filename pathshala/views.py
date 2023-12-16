from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, StudentSerializer, MentorStudentSerializer, BhaagSerializer, SessionSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action 
from django.contrib.auth import authenticate
from .models import Student, Mentor, Parent, Volunteer

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


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Implement user login logic
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response={
                "status": "success",
                "message": "Login successful",
                "data": {'access_token': access_token, 'refresh_token': refresh_token},
            }
            return Response(response)
        else:
            # Authentication failed
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
        serializer = UserSerializer(request.user, data=request.data, partial=True)
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
        from .models import Session
        
        if session_date:=request.GET.get('date'):
            session_objects = Session.objects.filter(date=session_date)
        else:
            session_objects = Session.objects.all()
        serializer = SessionSerializer(session_objects, many=True)

        response={
            "status": "success",
            "message": "Session fetch successful",
            "data": serializer.data 
        }
        return Response(response, status=status.HTTP_200_OK)




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
            date=request_data.get('date')
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
                        Attendance.objects.create(student=student, session=session, status=True)
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

# class LocationAPIView(APIView):
