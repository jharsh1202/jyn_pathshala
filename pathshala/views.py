from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, StudentSerializer, MentorStudentSerializer
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
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            return Response({'success': True, 'access_token': access_token, 'refresh_token': refresh_token})
        else:
            # Authentication failed
            return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RoleProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        data=request.data
        user_profile=user.profile

        if user_profile.role == 'Student':
            student=Student.objects.create(profile=user_profile)
            student.bhaag_class_id = data.get('bhaag_class') #TODO
            student.save() #TODO Trigger for review
        if user_profile.role == 'Mentor':
            from .models import BhaagClass, BhaagCategory, Location
            bhaag_class=BhaagClass.objects.get(bhaag_category=BhaagCategory.objects.get(bhaag_id=data.get('bhaag_id'), category=data.get('bhaag_category')), location=Location.objects.get(id=data.get('location_id')))
            mentor=Mentor.objects.create(profile=user_profile, bhaag_class=bhaag_class) #TODO
            mentor.save() 
        return Response("profile created successfully")
class StudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mentor=Mentor.objects.get(profile=request.user.profile)
        students=Student.objects.filter(bhaag_class=mentor.bhaag_class)
        serializer = MentorStudentSerializer(students, many=True)
        return Response(serializer.data)


# class LocationAPIView(APIView):
