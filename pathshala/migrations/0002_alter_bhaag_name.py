# Generated by Django 4.2.7 on 2023-12-11 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathshala', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bhaag',
            name='name',
            field=models.CharField(choices=[('Bhag 1 Oral Prelims - A', 'Bhag 1 Oral Prelims - A'), ('Bhag 1 Oral Prelims - B', 'Bhag 1 Oral Prelims - B'), ('Bhag 1 Advanced', 'Bhag 1 Advanced'), ('Bhag 2 Advanced', 'Bhag 2 Advanced'), ('Bhag 3 Prelims', 'Bhag 3 Prelims'), ('Bhag 4 Prelims', 'Bhag 4 Prelims'), ('Bhag 5 Prelims', 'Bhag 5 Prelims'), ('Bhag 6 Prelims', 'Bhag 6 Prelims')], max_length=50, unique=True),
        ),
    ]
