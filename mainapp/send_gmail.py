from django.core.mail import EmailMessage
from django.conf import settings


def end_msgs(email):
    mail = EmailMessage(
        'Hello',
        'привет ты успешно зарегистрировался!',
        settings.EMAIL_HOST_USER,
        [email]
    )
    mail.attach_file('mainapp/text.txt') #для отправки файлов б в скобках путь
    mail.send()