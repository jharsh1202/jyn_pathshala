from django.contrib import admin
from .models import UserProfile, Bhaag, Student, Mentor, Parent, Volunteer

admin.site.register(UserProfile)
admin.site.register(Bhaag)
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Parent)
admin.site.register(Volunteer)
