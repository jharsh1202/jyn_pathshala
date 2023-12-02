from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    role_choices = [
        ('Admin', 'Admin'),
        ('Mentor', 'Mentor'),
        ('Co-Mentor', 'Co-Mentor'),
        ('Volunteer', 'Volunteer'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=20, choices=role_choices)
    dob = models.DateField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    blood_group_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=5)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.profile_picture:
            username = self.user.username if self.user else 'unknown_user'
            timestamp = str(int(timezone.now().timestamp()))
            file_extension = os.path.splitext(self.profile_picture.name)[1]
            filename = f'profile_pics/{username}_{timestamp}{file_extension}'

            self.profile_picture.name = filename

        super().save(*args, **kwargs)
