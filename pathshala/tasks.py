# your_app/tasks.py

from django.core.management.base import BaseCommand
from .models import Session, Bhaag, BhaagCategory, BhaagClass, Mentor, UserProfile
from celery import Celery
from celery.utils.log import get_task_logger
from django.core.management import call_command

app = Celery('pathshala')
logger = get_task_logger(__name__)

@app.task
def create_session_records():
    from datetime import datetime

    current_date_time = datetime.now()
    current_date = current_date_time.date()

    for bhaag_class in BhaagClass.objects.all():
        class_mentor=Mentor.objects.get(bhaag_class=bhaag_class)
        Session.objects.create(date=current_date, bhaag_class=bhaag_class, day_mentor=class_mentor)
