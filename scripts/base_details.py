# INSIDE SHELL
# exec(open('scripts/base_details.py').read())

import pandas as pd

from datetime import datetime
import random
from pathshala.models import Student, UserProfile, User, BhaagClass, Bhaag, BhaagCategory, Location, Group, BhaagClassSection, Mentor
from django.db import transaction
try:
    for name in ['Student', 'Mentor', 'Admin', 'Volunteer', 'Member', 'Parent', 'Swadhyay']:
        group, created = Group.objects.get_or_create(name=name)
    
    # BASE DATA :) # !!IMPORTANT
    first_name="Preeti"
    last_name="Jain"
    dob='1983-01-03'
    user_name=(first_name+"_"+dob).lower().replace("-", "_")
    user=User.objects.create(username=user_name,email=user_name+'@jynpathshala.com')
    user.set_password('Raipur@123')
    user.save()
    user_profile=UserProfile(
        user=user, 
        first_name=first_name, 
        last_name=last_name,
        dob=dob,
        phone='8826996224',
        email=user_name+'@jynpathshala.com',
        date_of_joining='2012-01-01'
    )
    user_profile.save()
    user_profile.groups.set([Group.objects.get(name='Mentor')])
    Mentor.objects.create(profile=user_profile)
            

    with transaction.atomic():

        location=Location.objects.create(street_address="Sector 27", city="Noida", state="Uttar Pradesh", country="India")

        for bhag in Bhaag.BHAG_CHOICES:
            bhag=Bhaag.objects.create(name=bhag[0], book='https://www.africau.edu/images/default/sample.pdf') #UPDATE URLS
            for bhag_mode in BhaagCategory.SESSION_CATEGORIES:
                print("mode--", bhag_mode)
                bhag_category=BhaagCategory.objects.create(bhaag=bhag, category=bhag_mode[0])
                for location in Location.objects.all():
                    print("location--", location)
                    bhag_class=BhaagClass.objects.create(bhaag_category=bhag_category, location=location)
                    for section in ['A']: #TODO DYANMIC MANUALLY ADD SECTION B FOR BHAG 1 ORAL PRELIMS AS PER DEC 2023
                        bhag_class_section=BhaagClassSection.objects.create(bhaag_class=bhag_class, section=section, primary_owner=Mentor.objects.get(profile__first_name='Preeti'))
                        if bhag.name == 'Bhag 1 Oral Prelims' and bhag_category.category=='online':
                            bhag_class_section=BhaagClassSection.objects.create(bhaag_class=bhag_class, section='B', primary_owner=Mentor.objects.get(profile__first_name='Preeti'))
        print('base data created', 'create a section B for bhag 1 oral prelims')
except Exception as e:
    import os, sys
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception Found: %s %s %s %s', exc_type,fname, exc_tb.tb_lineno)
    print(f"Error reading Excel file: {e}")