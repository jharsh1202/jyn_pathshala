# Generated by Django 4.2.7 on 2023-12-03 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bhaag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Bhag 1 Oral Prelims - A', 'Bhag 1 Oral Prelims - A'), ('Bhag 1 Oral Prelims - B', 'Bhag 1 Oral Prelims - B'), ('Bhag 1 Advanced', 'Bhag 1 Advanced'), ('Bhag 2 Advanced', 'Bhag 2 Advanced'), ('Bhag 3 Prelims', 'Bhag 3 Prelims'), ('Bhag 4 Prelims', 'Bhag 4 Prelims'), ('Bhag 5 Prelims', 'Bhag 5 Prelims'), ('Bhag 6 Prelims', 'Bhag 6 Prelims')], max_length=50)),
                ('book', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='BhaagCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('offline', 'offline'), ('online', 'online')], max_length=20)),
                ('bhaag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathshala.bhaag')),
            ],
        ),
        migrations.CreateModel(
            name='BhaagClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bhaag_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathshala.bhaagcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bhaag_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pathshala.bhaagclass')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Mentor', 'Mentor'), ('Co-Mentor', 'Co-Mentor'), ('Volunteer', 'Volunteer'), ('Member', 'Member'), ('Student', 'Student')], max_length=20)),
                ('dob', models.DateField()),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=5)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('date_of_joining', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer', to='pathshala.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bhaag_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pathshala.bhaagclass')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='student', to='pathshala.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('bhaag_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pathshala.bhaagclass')),
                ('day_mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_mentor', to='pathshala.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children', models.ManyToManyField(related_name='parents', to='pathshala.student')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='pathshala.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='mentor',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to='pathshala.userprofile'),
        ),
        migrations.AddField(
            model_name='bhaagclass',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='pathshala.location'),
        ),
        migrations.CreateModel(
            name='Attendnace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session', to='pathshala.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='pathshala.student')),
            ],
        ),
    ]