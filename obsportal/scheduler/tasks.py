from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_mail(self, target_mail, message):
    mail_subject = "Test Mail Complete!"
    send_mail(
        subject = mail_subject,
        message = message,
        from_email = 'from@example.com',
        recipient_list = [target_mail],
        fail_silently = False,
        )

