from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from .mixins import RegistrationRoleMixin
import os
from django.core.exceptions import ValidationError
from datetime import time


class CreateUpdateAtAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated_by')

    class Meta:
        abstract = True


class ActiveInactiveAbstractModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class HistoryStatusAbstractModel(CreateUpdateAtAbstractModel, TimestampedModel, ActiveInactiveAbstractModel):

    class Meta:
        abstract = True


class UserProfile(HistoryStatusAbstractModel):
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
    GENDER_CHOICES=[
        ("Female","Female"),
        ("Male","Male"),
        ("Other","Other")
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
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True) #DEFAULT IMAGE , default='profile_pics/default_dp.png'
    date_of_joining = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.profile_picture: #DEFAULT IMAGE and self.profile_picture.name!='profile_pics/default_dp.png'
            username = self.user.username if self.user else 'unknown_user'
            timestamp = str(int(timezone.now().timestamp()))
            file_extension = os.path.splitext(self.profile_picture.name)[1]
            filename = f'{username}_{timestamp}{file_extension}'
            self.profile_picture.name = filename
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"


class Location(HistoryStatusAbstractModel):
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.street_address} {self.city} {self.state}"
    
    class Meta:
        unique_together=["street_address", "city", "state", "country"]


class Bhaag(HistoryStatusAbstractModel):
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


class BhaagCategory(HistoryStatusAbstractModel):
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


class BhaagClass(HistoryStatusAbstractModel):
    bhaag_category = models.ForeignKey(BhaagCategory, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')

    def __str__(self):
        return f"{self.bhaag_category.bhaag.name} {self.bhaag_category.category} {self.location}"
    
    class Meta:
        unique_together=['bhaag_category', 'location']


class BhaagClassSection(HistoryStatusAbstractModel):
    bhaag_class = models.ForeignKey(BhaagClass, on_delete=models.CASCADE)
    section = models.CharField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E')
    ], max_length=1)
    primary_owner = models.ForeignKey("Mentor", on_delete=models.PROTECT)
    secondary_owner = models.ForeignKey("Mentor", on_delete=models.PROTECT, null=True, blank=True, related_name="secondary_owner")
    team = models.ManyToManyField("Mentor", related_name="team")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.primary_owner not in self.team.all():
            self.team.add(self.primary_owner)

    def clean(self):
        super().clean()
        if self.primary_owner not in self.team.all():
            raise ValidationError("Primary owner must be in the team.")

    def __str__(self):
        return f"{self.bhaag_class.bhaag_category.bhaag.name} {self.section} {self.bhaag_class.bhaag_category.category} {self.bhaag_class.location}"

    class Meta:
        unique_together=['section', 'bhaag_class']


class Student(RegistrationRoleMixin, HistoryStatusAbstractModel):
    group_name = "Student"
    profile = models.OneToOneField(UserProfile, on_delete=models.PROTECT, related_name='student')
    bhaag_class_section = models.ForeignKey(BhaagClassSection, on_delete=models.PROTECT, related_name='bhaag_class_section')

    def __str__(self):
        return f"{self.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name} {self.bhaag_class_section.section} {self.bhaag_class_section.bhaag_class.bhaag_category.category} {self.profile.first_name} {self.profile.phone}"

    class Meta:
        unique_together = ["profile", "bhaag_class_section"]


class Mentor(RegistrationRoleMixin, HistoryStatusAbstractModel):
    group_name = "Mentor"

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='mentor', unique=True)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name} {self.profile.phone}"



class Parent(RegistrationRoleMixin, HistoryStatusAbstractModel):
    group_name = "Parent"
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='parent')
    children = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.phone}"


class Volunteer(RegistrationRoleMixin, HistoryStatusAbstractModel):
    group_name = "Volunteer"
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='volunteer')

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.phone}"


class Session(HistoryStatusAbstractModel):
    date = models.DateField()
    time = models.TimeField(default=time(10, 0))
    bhaag_class_section = models.ForeignKey(BhaagClassSection, on_delete=models.PROTECT)
    # session_type = models.CharField(choices={
    #     ('regular', 'regular'),
    #     ('activity', 'activity'),
    #     ('trip', 'trip')
    # }, max_length=20)
    day_mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='day_mentor')

    def __str__(self):
        return f"{self.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name} {self.bhaag_class_section.bhaag_class.bhaag_category.category} {self.date} {self.day_mentor}"

    class Meta:
        unique_together = ["date", "bhaag_class_section"]


class Attendance(HistoryStatusAbstractModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session')
    status = models.BooleanField()

    def __str__(self):
        return f"{self.student.profile.first_name} {self.session.bhaag_class_section.bhaag_class.bhaag_category.bhaag.name} {self.status}"

    class Meta:
        unique_together = ["student", "session", "status"]


class VideoBhaag(HistoryStatusAbstractModel):
    bhaag = models.ManyToManyField(Bhaag, related_name='video_bhaag')
    title = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    category = models.CharField(choices=[
        ("festival", "festival"),
        ("historical", "historical"),
        ("moral", "moral"),
        ("story", "story"),
    ], max_length=100)

    def __str__(self):
        return f"{self.title} {self.category} {self.bhaag.name}"


class ResourceBhaag(HistoryStatusAbstractModel):
    bhaag = models.ManyToManyField(Bhaag, related_name='resource_bhaag')
    title = models.CharField(max_length=100, unique=True)
    text = models.TextField(null=True) 
    category = models.CharField(choices=[
        ("jinvani", "jinvani"),
        ("kavita", "kavita"),
        ("bhajan", "bhajan"),
        ("stuti", "stuti"),
        ("pooja", "pooja"),
        ("chalisa", "chalisa"),
        ("facts", "facts"),
    ], max_length=100)
    resource_type = models.CharField(choices=[
        ("text", "text"),
    ], max_length=100)

    def __str__(self):
        return f"{self.title} {self.bhaag.name}"