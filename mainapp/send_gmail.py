from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task


@shared_task
def end_msgs(email):
    mail = EmailMessage(
        'Hello',
        'привет ты успешно зарегистрировался!',
        settings.EMAIL_HOST_USER,
        [email]
    )
    mail.attach_file('mainapp/text.txt') #для отправки файлов б в скобках путь
    mail.send()