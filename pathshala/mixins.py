from django.db import models
from django.core.exceptions import ValidationError
class RegistrationRoleMixin: 

    def __init__(self, *args, **kwargs):
        if not hasattr(self.__class__, 'group_name') or getattr(self.__class__, 'group_name') is None:
            raise AttributeError(f"Class variable 'group_name' not defined or is None in {self.__class__}")

    def validate_registration_role(self):
        from .models import Group
        group_student = Group.objects.get(name=self.group_name)
        if group_student not in self.profile.groups.all():
            raise ValidationError(f"Invalid Registration Group. Must be a '{self.group_name}', Contact ADMIN.")

    def clean(self):
        self.validate_registration_role()
        return super().clean()