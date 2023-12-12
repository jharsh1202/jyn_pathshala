from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .mixins import RegistrationRoleMixin
import os

class UserProfile(models.Model):

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
    groups = models.ManyToManyField(Group)
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=15, blank=True, null=True) 
    alias = models.CharField(max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True, choices=BLOOD_GROUP_CHOICES)
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"


class Location(models.Model):
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.street_address} {self.city} {self.state}"
    
    class Meta:
        unique_together=["street_address", "city", "state", "country"]


class Bhaag(models.Model):
    BHAG_CHOICES = (
        ('Bhag 1 Oral Prelims', 'Bhag 1 Oral Prelims'),
        ('Bhag 1 Advanced', 'Bhag 1 Advanced'),
        ('Bhag 2 Advanced', 'Bhag 2 Advanced'),
        ('Bhag 3 Prelims', 'Bhag 3 Prelims'),
        ('Bhag 4 Prelims', 'Bhag 4 Prelims'),
        ('Bhag 5 Prelims', 'Bhag 5 Prelims'),
        ('Bhag 6 Prelims', 'Bhag 6 Prelims'),
    )

    name = models.CharField(max_length=50, choices=BHAG_CHOICES, unique=True)
    book = models.URLField()

    def __str__(self):
        return f"{self.name}"
    

class BhaagCategory(models.Model):
    SESSION_CATEGORIES = [
        ('offline', 'offline'),
        ('online', 'online'),
    ]
    bhaag = models.ForeignKey(Bhaag, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=SESSION_CATEGORIES)

    def __str__(self):
        return f"{self.bhaag.name} {self.category}"
    
    class Meta:
        unique_together=["bhaag", "category"]


class BhaagClass(models.Model):
    bhaag_category = models.ForeignKey(BhaagCategory, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')

    def __str__(self):
        return f"{self.bhaag_category.bhaag.name} {self.bhaag_category.category} {self.location}"
    
    class Meta:
        unique_together=['bhaag_category', 'location']


class BhaagClassSection(models.Model):
    bhaag_class = models.ForeignKey(BhaagClass, on_delete=models.CASCADE)
    section = models.CharField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E')
    ], max_length=1)

    def __str__(self):
        return f"{self.bhaag_class.bhaag_category.bhaag.name} {self.section} {self.bhaag_class.bhaag_category.category} {self.bhaag_class.location}"

    class Meta:
        unique_together=['section', 'bhaag_class']

class Student(RegistrationRoleMixin, models.Model):
    group_name = "Student"
    profile = models.OneToOneField(UserProfile, on_delete=models.PROTECT, related_name='student')
    bhaag_class_section = models.ForeignKey(BhaagClassSection, on_delete=models.PROTECT, related_name='bhaag_class_section')

    def __str__(self):
        return f"{self.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name} {self.bhaag_class_section.section} {self.bhaag_class_section.bhaag_class.bhaag_category.category} {self.profile.first_name} {self.profile.phone}"

    class Meta:
        unique_together = ["profile", "bhaag_class_section"]


class Mentor(RegistrationRoleMixin, models.Model):
    group_name = "Mentor"
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='mentor')
    bhaag_class_section = models.ForeignKey(BhaagClassSection, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.profile.first_name} {self.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name}"

    class Meta:
        unique_together = ["profile", "bhaag_class_section"]

class Parent(RegistrationRoleMixin, models.Model):
    group_name = "Parent"
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='parent')
    children = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.phone}"


class Volunteer(RegistrationRoleMixin, models.Model):
    group_name = "Volunteer"
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='volunteer')

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.phone}"


class Session(models.Model):
    date = models.DateField()
    bhaag_class_section = models.ForeignKey(BhaagClassSection, on_delete=models.PROTECT)
    day_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='day_mentor')

    def __str__(self):
        return f"{self.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name} {self.date} {self.day_mentor}"

    class Meta:
        unique_together = ["date", "bhaag_class_section", "day_mentor"]

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session')
    status = models.BooleanField()

    def __str__(self):
        return f"{self.student.profile.first_name} {self.session.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name} {self.status}"

    class Meta:
        unique_together = ["student", "session", "status"]