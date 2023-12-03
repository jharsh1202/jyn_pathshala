from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Mentor', 'Mentor'),
        ('Co-Mentor', 'Co-Mentor'),
        ('Volunteer', 'Volunteer'),
        ('Member', 'Member'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dob = models.DateField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.profile_picture:
            username = self.user.username if self.user else 'unknown_user'
            timestamp = str(int(timezone.now().timestamp()))
            file_extension = os.path.splitext(self.profile_picture.name)[1]
            filename = f'profile_pics/{username}_{timestamp}{file_extension}'

            self.profile_picture.name = filename

        super().save(*args, **kwargs)


class Bhaag(models.Model):
    BHAG_CHOICES = (
        ('Bhag 1 Oral Prelims - A', 'Bhag 1 Oral Prelims - A'),
        ('Bhag 1 Oral Prelims - B', 'Bhag 1 Oral Prelims - B'),
        ('Bhag 1 Advanced', 'Bhag 1 Advanced'),
        ('Bhag 2 Advanced', 'Bhag 2 Advanced'),
        ('Bhag 3 Prelims', 'Bhag 3 Prelims'),
        ('Bhag 4 Prelims', 'Bhag 4 Prelims'),
        ('Bhag 5 Prelims', 'Bhag 5 Prelims'),
        ('Bhag 6 Prelims', 'Bhag 6 Prelims'),
    )
    SESSION_CATEGORIES = [
        ('offline', 'offline'),
        ('online', 'online'),
    ]
    name = models.CharField(max_length=50, unique=True, choices=BHAG_CHOICES)
    book = models.URLField()
    category = models.CharField(max_length=20, choices=SESSION_CATEGORIES)

class Student(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.PROTECT, related_name='student')
    bhaag = models.ForeignKey(Bhaag, on_delete=models.PROTECT)


class Mentor(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='mentor')
    bhaag = models.ForeignKey(Bhaag, on_delete=models.PROTECT)


class Parent(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='parent')
    children = models.ManyToManyField(Student, related_name='parents')

class Volunteer(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='volunteer')
    

class Session(models.Model):
    date = models.DateField()
    bhaag = models.ForeignKey(Bhaag, on_delete=models.CASCADE)
    day_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='day_mentor')

class Attendnace(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session')
    status = models.BooleanField()
