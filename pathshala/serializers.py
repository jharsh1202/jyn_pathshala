from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Student, BhaagClass, Bhaag, BhaagCategory, Location, Group, Session, Attendance, BhaagClassSection, Mentor
from django.db import transaction


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user', )


class BhaagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bhaag
        exclude = ()


class BhaagCategorySerializer(serializers.ModelSerializer):
    bhaag = BhaagSerializer()
    class Meta:
        model = BhaagCategory
        exclude = ('id', )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ('id', )


class BhaagClassSerializer(serializers.ModelSerializer):
    bhaag_category = BhaagCategorySerializer()
    location = LocationSerializer()
    class Meta:
        model = BhaagClass
        exclude = ()

class BhaagClassSectionSerializer(serializers.ModelSerializer):
    bhaag_class = BhaagClassSerializer()
    class Meta:
        model = BhaagClassSection
        exclude = ()


class StudentSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    bhaag_class_section = BhaagClassSectionSerializer()

    class Meta:
        model = Student
        exclude = ()


class MentorSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = Mentor
        exclude = ()


class MentorStudentSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    bhaag_class_section = BhaagClassSectionSerializer()

    class Meta:
        model = Student
        exclude = ()


class SessionSerializer(serializers.ModelSerializer):    
    bhaag_class_section = BhaagClassSectionSerializer()
    day_mentor = MentorSerializer()
    class Meta:
        model = Session
        exclude = ()


class AttendanceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Attendance
        exclude = ()


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.get('profile')
        group = profile_data.pop('groups')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        user_profile = UserProfile.objects.create(user=user, **profile_data)
        user_profile.groups.set(group)
        return user
    
    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update User model fields
        # instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update UserProfile model fields
        if profile_data:
            profile_instance = instance.profile
            profile_serializer = UserProfileSerializer(profile_instance, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()

        return instance