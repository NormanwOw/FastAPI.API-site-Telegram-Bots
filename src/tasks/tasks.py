import smtplib

from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = 'smtp.yandex.ru'
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email(order: dict):
    email = EmailMessage()
    email['Subject'] = f'Telegram-bots | Заказ №{order["order_id"]}'
    email['From'] = SMTP_USER
    email['To'] = order['email']

    del order['email'], order['date']

    with open('src/templates/mail.html', 'rb') as mail:
        msg = mail.read().decode('utf-8')
        msg = msg.format(*order.values())
        email.set_content(msg, subtype='html')
    return email


@celery.task
def send_email(order: dict):
    email = get_email(order)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as mail:
        mail.login(SMTP_USER, SMTP_PASSWORD)
        mail.send_message(email)
