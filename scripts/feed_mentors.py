# INSIDE SHELL
# PUT master db CSV scripts/jyn_db_students.csv
# exec(open('scripts/feed_mentors.py').read())

import pandas as pd

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
from pathshala.models import Student, UserProfile, User, BhaagClass, Bhaag, BhaagCategory, Location, Group, BhaagClassSection, Mentor
from django.db import transaction
try:
    mentors_excel_file_path = 'scripts/jyn_db_mentors.csv'
    df1 = pd.read_csv(mentors_excel_file_path)

    mentor_group=Group.objects.get(name='Mentor')
    with transaction.atomic():
        for index, row in df1.iterrows():
            mentor_name=row['name'].split()
            if len(mentor_name)==2:    
                first_name=mentor_name[0]
                last_name=mentor_name[1]
            else:
                first_name=mentor_name[0]
                middle_name=mentor_name[1]
                last_name=mentor_name[2]

            # class_mode=row['class_mode']
            dob=row['dob']
            mobile_no=row['mobile_no']
            city=row['city']
            address=row['address']
            doj=row['doj']
            user_name=(first_name+"_"+dob).lower().replace("-", "_")
            print(user_name)
            user=User.objects.create(username=user_name,email=user_name+'@jynpathshala.com')
            user.set_password('Raipur@123')
            user.save()
            user_profile=UserProfile(
                user=user, 
                first_name=first_name, 
                last_name=last_name,
                dob=dob,
                phone=mobile_no,
                email=user_name+'@jynpathshala.com',
                date_of_joining=doj
            )
            user_profile.save()
            user_profile.groups.set([mentor_group])
            Mentor.objects.create(profile=user_profile)
except Exception as e:
    print('Exception', e)
    import os, sys
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception Found: %s %s %s %s', exc_type,fname, exc_tb.tb_lineno)
    print(f"Error reading Excel file: {e}")
    df = None