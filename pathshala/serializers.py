from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Student, BhaagClass, Bhaag, BhaagCategory, Location, Group, Session, Attendance, \
    BhaagClassSection, Mentor, VideoBhaag, ResourceBhaag
from django.db import transaction


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('user', 'created_at', 'updated_at', 'created_by', 'updated_by')


class BhaagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bhaag
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


class BhaagCategorySerializer(serializers.ModelSerializer):
    bhaag = BhaagSerializer()
    class Meta:
        model = BhaagCategory
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', )


class BhaagClassSerializer(serializers.ModelSerializer):
    bhaag_category = BhaagCategorySerializer()
    location = LocationSerializer()
    class Meta:
        model = BhaagClass
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


class MentorSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = Mentor
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


class BhaagClassSectionSerializer(serializers.ModelSerializer):
    bhaag_class = BhaagClassSerializer()
    team = MentorSerializer(many=True)
    class Meta:
        model = BhaagClassSection
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


class StudentSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    bhaag_class_section = BhaagClassSectionSerializer()

    class Meta:
        model = Student
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')




class MentorStudentSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    bhaag_class_section = BhaagClassSectionSerializer()
    attendance = serializers.SerializerMethodField()

    def get_attendance(self, obj):
        return Attendance.calculate_bhg_cls_sec_student_attendance(student_id=obj.id)

    class Meta:
        model = Student
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


class VideoBhaagSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoBhaag
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


class SessionSerializer(serializers.ModelSerializer):    
    day_mentor_id = serializers.IntegerField(write_only=True) #for updating mentor id 

    bhaag_class_section = BhaagClassSectionSerializer()
    day_mentor = MentorSerializer(read_only=True)
    class Meta:
        model = Session
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def update(self, instance, validated_data):
        day_mentor_data = validated_data.pop('day_mentor', None)
        if day_mentor_data:
            instance.day_mentor = Mentor.objects.get(id=day_mentor_data.get('id'))
            instance.save()
        return super().update(instance, validated_data)


class AttendanceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Attendance
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')


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


class ResourceBhaagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResourceBhaag
        fields = ['id', 'title']


class ResourceBhaagTextSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResourceBhaag
        fields = ['id', 'title', 'text']
