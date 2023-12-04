from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Student, BhaagClass, Bhaag, BhaagCategory, Location
from django.db import transaction


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
        exclude = ('id', )


class StudentSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    bhaag_class = BhaagClassSerializer()

    class Meta:
        model = Student
        exclude = ()
    

class MentorStudentSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    bhaag_class = BhaagClassSerializer()

    class Meta:
        model = Student
        exclude = ()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, **profile_data)
        return user