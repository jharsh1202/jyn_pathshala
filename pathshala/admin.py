from django.contrib import admin
from .models import UserProfile, Bhaag, Student, Mentor, Parent, Volunteer, Session, Attendance, BhaagCategory, BhaagClass, Location

admin.site.register(UserProfile)
admin.site.register(Bhaag)
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Parent)
admin.site.register(Volunteer)
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(BhaagClass)
admin.site.register(BhaagCategory)
admin.site.register(Location)
