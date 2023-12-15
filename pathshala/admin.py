from django.contrib import admin
from .models import UserProfile, Bhaag, Student, Mentor, Parent, Volunteer, Session, Attendance, BhaagCategory, BhaagClass, Location, BhaagClassSection, Group


class BhaagClassSectionFilter(admin.SimpleListFilter):
    title = 'Bhaag Class Section'
    parameter_name = 'bhaag_class_section'

    def lookups(self, request, model_admin):
        sections = BhaagClassSection.objects.values_list('id', 'bhaag_class__bhaag_category__bhaag__name', 'section', 'bhaag_class__bhaag_category__category')
        formatted_sections = [ ( id, f"{bhaag_name} {section} {category}" ) for id, bhaag_name, section, category in sections ]
        return tuple(formatted_sections)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bhaag_class_section_id=self.value())


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_student_info', 'bhaag_class_section']
    list_filter = [BhaagClassSectionFilter]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'profile':
            mentor_group_id = Group.objects.get(name="Student")
            kwargs['queryset'] = UserProfile.objects.filter(id__in=UserProfile.objects.filter(groups__in=[mentor_group_id]).all().exclude(id__in=Student.objects.all().values('id'))) 

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_student_info(self, obj):
        return str(obj)
    get_student_info.short_description = 'Student Info'


class MentorAdmin(admin.ModelAdmin):
    list_display = ['profile', 'bhaag_class_section']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'profile':
            mentor_group_id = Group.objects.get(name="Mentor")
            kwargs['queryset'] = UserProfile.objects.filter(id__in=UserProfile.objects.filter(groups__in=[mentor_group_id]).all()).exclude(id__in=Mentor.objects.values('profile')) #filter(your_condition_here=user_profile)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Mentor, MentorAdmin)


admin.site.register(Parent)
admin.site.register(Volunteer)
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(BhaagClass)
admin.site.register(BhaagCategory)
admin.site.register(Location)
admin.site.register(BhaagClassSection)
admin.site.register(Student, StudentAdmin)
admin.site.register(UserProfile)
admin.site.register(Bhaag)