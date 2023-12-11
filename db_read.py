import pandas as pd

# Specify the path to your Excel file
excel_file_path = 'jyn_db1.csv'

# Define the expected column names
# expected_columns = [
#     "S.No.",
#     "Student Name",
#     "Bhag Name",
#     "Gurdian's Name",
#     "Class Mode",
#     "Joining month",
#     "DOB",
#     "Age in years",
#     "Mobile no.",
#     "City",
#     "Address",
# ]


def convert_date_format(input_date):
    try:
        if input_date in ("", " ", None) or type(input_date)==type(1.0): 
            # print("input_date", input_date)
            return None
        # Parse the input date string
        try:
        # print(type(input_date), input_date)
            parsed_date = datetime.strptime(input_date, '%b-%Y')
        except:
            parsed_date = datetime.strptime(input_date, '%b %Y')

        # Format the date as "01-MM-YY"
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
        # Try to parse the date in DMY format
        original_date = datetime.strptime(date_string, "%d-%m-%Y")
        
        # Format the date in YMD format
        formatted_date = original_date.strftime("%Y-%m-%d")
        
        return formatted_date
    except ValueError:
        # Handle the case where the format is not DMY
        # print("Invalid date format. Please provide a date in the format 'day-month-year'.")
        return date_string

# Example usage
# # original_date_string = "27-07-2016"
# # formatted_date = convert_to_ymd(original_date_string)

# if formatted_date:
#     print("Original Date:", original_date_string)
    # print("Formatted Date:", formatted_date)



# Read the Excel file into a DataFrame

from datetime import datetime
from pathshala.models import Student, UserProfile, User, BhaagClass, Bhaag, BhaagCategory, Location, Group
from django.db import transaction
try:


    for name in ['Student', 'Mentor', 'Admin', 'Volunteer', 'Member', 'Parent']:
        group, created = Group.objects.get_or_create(name=name)
    

    #create bhags
            

    with transaction.atomic():
        location=Location.objects.create(street_address="Sector 27", city="Noida", state="Uttar Pradesh", country="India")
        
        for bhag in Bhaag.BHAG_CHOICES:
            bhag=Bhaag.objects.create(name=bhag[0], book='https://www.africau.edu/images/default/sample.pdf')
            for bhag_mode in BhaagCategory.SESSION_CATEGORIES:
                print("mode--", bhag_mode)
                bhag_category=BhaagCategory.objects.create(bhaag=bhag, category=bhag_mode[0])
                for location in Location.objects.all():
                    print("location--", location)
                    bhag_class=BhaagClass.objects.create(bhaag_category=bhag_category, location=location)
    
    print('base data created')
    df = pd.read_csv(excel_file_path)
    # print(df[:5])
    

    group=Group.objects.get(name='Student')
    with transaction.atomic():
        for index, row in df.iterrows():
            student_name=row['Student Name']
            bhag_name=row['Bhag Name']
            class_mode=row['Class Mode']
            dob=convert_to_ymd(row['DOB'])
            mobile=row['Mobile no.']
            city=row['City']
            address=row['Address']
            doj=convert_date_format(row['Joining month'])

            original_date_string = "27-07-2016"

            original_date = datetime.strptime(original_date_string, "%d-%m-%Y")
            formatted_date_string = original_date.strftime("%Y-%m-%d")

            doj = '2023-01-01' if doj else doj #TODO IMPORTANT!!
            doj_user_name=doj
            user_name = student_name.split()[0].lower()+doj
            print(user_name, student_name, bhag_name, class_mode, dob, mobile, city, address, doj)
            # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
            # first_name = models.CharField(max_length=30)
            # middle_name = models.CharField(max_length=30, blank=True, null=True)
            # last_name = models.CharField(max_length=30)
            # groups = models.ManyToManyField(Group)
            # dob = models.DateField()
            # phone = models.CharField(max_length=15, blank=True, null=True) 
            # alias = models.CharField(max_length=15, blank=True, null=True, unique=True)
            # email = models.EmailField(unique=True, blank=True, null=True)
            # blood_group = models.CharField(max_length=5, blank=True, null=True, choices=BLOOD_GROUP_CHOICES)
            # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
            # date_of_joining =
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
            # book = models.URLField()
            bhag=Bhaag.objects.get(name=bhag_name)
            bhaag_category=BhaagCategory.objects.get(bhaag=bhag, category=class_mode)
            location=Location.objects.get(street_address='Sector 27')
            bhaag_class=BhaagClass.objects.get(bhaag_category=bhaag_category, location=location)
            student=Student.objects.create(profile=user_profile, bhaag_class=bhaag_class)

except Exception as e:
    import os, sys
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print('Exception Found: %s %s %s %s', exc_type,fname, exc_tb.tb_lineno)
    print(f"Error reading Excel file: {e}")
    df = None

# # Check if the columns match the expected columns
# if df is not None and set(expected_columns).issubset(df.columns):
#     # DataFrame contains the expected columns
#     print("Excel file read successfully.")
#     print(df.head())  # Display the first few rows of the DataFrame
# else:
#     print("Error: Excel file does not have the expected columns.")



# Example usage:
# input_string = "Aug-2023"
# output_string = convert_date_format(input_string)

# print(output_string)
