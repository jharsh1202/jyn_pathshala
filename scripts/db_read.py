import pandas as pd

# Specify the path to your Excel file
excel_file_path = 'jyn_db.csv'


def convert_date_format(input_date):
    try:
        if input_date in ("", " ", None) or type(input_date)==type(1.0):
            return None
        try:
            parsed_date = datetime.strptime(input_date, '%b-%Y')
        except:
            try:
                parsed_date = datetime.strptime(input_date, '%b %Y')
            except:
                return None
        formatted_date = parsed_date.strftime('01-%m-%y')
        return formatted_date
    except Exception as e:
        import os, sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception Found: %s %s %s %s', exc_type,fname, exc_tb.tb_lineno)
        print("---", e, input_date)


def convert_to_ymd(date_string):
    try:
        original_date = datetime.strptime(date_string, "%d/%m/%Y")
        formatted_date = original_date.strftime("%Y-%m-%d")
        return formatted_date
    except ValueError:
        return date_string

from datetime import datetime
import random
from pathshala.models import Student, UserProfile, User, BhaagClass, Bhaag, BhaagCategory, Location, Group, BhaagClassSection
from django.db import transaction
try:
    for name in ['Student', 'Mentor', 'Admin', 'Volunteer', 'Member', 'Parent']:
        group, created = Group.objects.get_or_create(name=name)
    
    # BASE DATA :) # !!IMPORTANT
            

    # with transaction.atomic():

    #     location=Location.objects.create(street_address="Sector 27", city="Noida", state="Uttar Pradesh", country="India")

    #     for bhag in Bhaag.BHAG_CHOICES:
    #         bhag=Bhaag.objects.create(name=bhag[0], book='https://www.africau.edu/images/default/sample.pdf')
    #         for bhag_mode in BhaagCategory.SESSION_CATEGORIES:
    #             print("mode--", bhag_mode)
    #             bhag_category=BhaagCategory.objects.create(bhaag=bhag, category=bhag_mode[0])
    #             for location in Location.objects.all():
    #                 print("location--", location)
    #                 bhag_class=BhaagClass.objects.create(bhaag_category=bhag_category, location=location)
    #                 for section in ['A']: #TODO DYANMIC
    #                     bhag_class_section=BhaagClassSection.objects.create(bhaag_class=bhag_class, section=section)
    #     print('base data created', 'create a section B for bhag 1 oral prelims')


    df = pd.read_csv(excel_file_path)

    group=Group.objects.get(name='Student')
    with transaction.atomic():
        for index, row in df.iterrows():
            if row['Bhag Name']=='Chhahdhala': continue #ONLY ALLOWING BHAAG STUDENTS
            student_name=row['Student Name']
            bhag_name=row['Bhag Name']
            class_mode=row['Class Mode'].lower()
            dob=convert_to_ymd(row['DOB'])
            print('d0b-----', dob)
            mobile=row['Mobile no.']
            city=row['City']
            address=row['Address']
            section=row['Section']
            doj=convert_date_format(row['Joining month'])

            original_date_string = "27-07-2016"

            original_date = datetime.strptime(original_date_string, "%d-%m-%Y")
            formatted_date_string = original_date.strftime("%Y-%m-%d")

            doj = '2023-01-01' if not doj else doj #TODO IMPORTANT!!
            doj_user_name=doj
            user_name = student_name.split()[0].lower()+"_"+doj+" "+dob+str(random.randint(100, 999))
            print(user_name, student_name, bhag_name, class_mode, dob, mobile, city, address, doj)
            user=User.objects.create(username=user_name,email=user_name+'@jynpathshala.com', password='RAIPUR@123')
            user_profile=UserProfile(user=user, first_name=student_name.split()[0], 
                                    last_name=student_name.split()[1],
                                    dob=dob,
                                    phone=mobile,
                                    email=user_name+'@jynpathshala.com',
                                    date_of_joining=doj
                                    )
            user_profile.save()
            user_profile.groups.set([group])
            bhag=Bhaag.objects.get(name=bhag_name)
            print('x-x-x-x-', bhag, class_mode)
            bhaag_category=BhaagCategory.objects.get(bhaag=bhag, category=class_mode)
            location=Location.objects.get(street_address='Sector 27')
            bhaag_class=BhaagClass.objects.get(bhaag_category=bhaag_category, location=location)
            print("-x-x-x-x-", bhaag_class, section)
            bhaag_class_section=BhaagClassSection.objects.get(bhaag_class=bhaag_class, section=section)
            student=Student.objects.create(profile=user_profile, bhaag_class_section=bhaag_class_section)
except Exception as e:
    import os, sys
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception Found: %s %s %s %s', exc_type,fname, exc_tb.tb_lineno)
    print(f"Error reading Excel file: {e}")
    df = None