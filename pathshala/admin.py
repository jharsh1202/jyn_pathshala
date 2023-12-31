from django.contrib import admin
from .models import UserProfile, Bhaag, Student, Mentor, Parent, Volunteer, Session, Attendance, BhaagCategory, BhaagClass, \
    Location, BhaagClassSection, Group, VideoBhaag


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


admin.site.register(Mentor)
admin.site.register(Parent)
admin.site.register(Volunteer)
class SessionAdmin(admin.ModelAdmin):
    list_filter = ('date', 'bhaag_class_section__bhaag_class__bhaag_category__category')

admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance)
admin.site.register(BhaagClass)
admin.site.register(BhaagCategory)
admin.site.register(Location)
class BhaagClassSectionAdmin(admin.ModelAdmin):
    list_filter = ('bhaag_class__bhaag_category__category', )

admin.site.register(BhaagClassSection, BhaagClassSectionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(UserProfile)
admin.site.register(Bhaag)
admin.site.register(VideoBhaag)