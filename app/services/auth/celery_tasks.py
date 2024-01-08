import asyncio
import random
import smtplib
from email.message import EmailMessage

from app.utils.my_celery import celery, settings
from app.utils.my_redis import get_redis


def _get_confirm_email_template(email_address: str, confirm_code: str):
    with open('confirmation_email_template.html', 'r') as file:
        email_content = file.read()

    email = EmailMessage()
    email['Subject'] = 'Подтверждение регистрации'
    email['From'] = settings.smtp_user
    email['To'] = settings.smtp_user  # FIX

    email.set_content(
        email_content.format(email_address=email_address, confirm_code=confirm_code),
        subtype='html'
    )
    return email


async def _set_and_expire(redis, email_address, confirm_code):
    await redis.set(email_address, confirm_code)
    await redis.expire(email_address, 5 * 60)


@celery.task()
def send_email_confirm(email_address):
    confirm_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    redis = get_redis()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_set_and_expire(redis, email_address, confirm_code))
    loop.close()

    email = _get_confirm_email_template(email_address, confirm_code)

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(email)
