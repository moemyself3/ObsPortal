from celery import shared_task
from django.core.mail import mail_admins

@shared_task
def send_admin_notification_mail(message):
    mail_subject = "Test Mail Complete!"
    mail_admins(
        subject = mail_subject,
        message = message,
        fail_silently = False,
        )

