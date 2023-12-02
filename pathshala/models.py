from django.db import models
from django.contrib.auth.models import User


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
