from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Student, Trainer, Training
import csv
import os


# Create your tasks here.

@shared_task
def send_email(recipient, message):
    subject = 'Skate School Notification'
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [recipient])


@shared_task
def generate_report():
    report_file = 'report.csv'
    with open(report_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Trainer', 'Date', 'Start Time', 'End Time', 'Students'])
        for training in Training.objects.all():
            writer.writerow([training.trainer.name, training.date, training.start_time, training.end_time,
                             training.students.count()])
    recipient = settings.EMAIL_HOST_USER
    subject = 'Skate School Report'
    message = f'Please find attached the report of all trainings.'
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [recipient], fail_silently=False, html_message=None,
              attachments=[(report_file, f.read(), 'text/csv')])


@shared_task
def backup_data():
    backup_file = 'backup.csv'
    with open(backup_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Model', 'Fields', 'Values'])
        for model in [Student, Trainer, Training]:
            for obj in model.objects.all():
                writer.writerow([model.__name__, obj._meta.fields, obj.__dict__])
    recipient = settings.EMAIL_HOST_USER
    subject = 'Skate School Backup'
    message = f'Please find attached the backup of all data.'
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [recipient], fail_silently=False, html_message=None,
              attachments=[(backup_file, f.read(), 'text/csv')])
