from django.contrib import admin
from .models import UserProfile, Bhaag, Student, Mentor, Parent, Volunteer, Session, Attendance, BhaagCategory, BhaagClass, Location, BhaagClassSection

class BhaagClassSectionFilter(admin.SimpleListFilter):
    title = 'Bhaag Class Section'
    parameter_name = 'bhaag_class_section'

    def lookups(self, request, model_admin):
        sections = BhaagClassSection.objects.values_list('id', 'bhaag_class__bhaag_category__bhaag__name')
        return tuple(sections)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bhaag_class_section_id=self.value())

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_student_info', 'bhaag_class_section']
    list_filter = [BhaagClassSectionFilter]

    def get_student_info(self, obj):
        return str(obj)
    get_student_info.short_description = 'Student Info'

# Register your models and admin site
admin.site.register(BhaagClassSection)
admin.site.register(Student, StudentAdmin)


# Register your models and admin site

admin.site.register(UserProfile)
admin.site.register(Bhaag)
# admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Parent)
admin.site.register(Volunteer)
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(BhaagClass)
admin.site.register(BhaagCategory)
admin.site.register(Location)
# admin.site.register(BhaagClassSection)
