# your_app/tasks.py

from django.core.management.base import BaseCommand
from pathshala.models import Session, Bhaag, BhaagCategory, BhaagClass, Mentor, UserProfile, BhaagClassSection
from celery import Celery
from celery.utils.log import get_task_logger
from django.core.management import call_command
from datetime import datetime, timedelta


app = Celery('pathshala')
logger = get_task_logger(__name__)

@app.task
def create_session_records():
    current_date = datetime.now()
    days_until_sunday = (6 - current_date.weekday() + 7) % 7
    next_sunday = current_date + timedelta(days=days_until_sunday)

    for bhaag_class_section in BhaagClassSection.objects.all():
        Session.objects.create(date=next_sunday, bhaag_class_section=bhaag_class_section, day_mentor=bhaag_class_section.primary_owner)
