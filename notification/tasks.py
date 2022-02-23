from celery import shared_task
from celery.utils.log import get_task_logger
#from django.core.mail import send_mail
from talent.models import Person


@shared_task(queue='notification', ignore_result=True)
def send_notification(notification_type, **kwargs):
    if notification_type == 'claim':
        email_receivers = list(Person.objects.values_list('email_address', flat=True).distinct('email_address').filter(id__in=kwargs['receivers']))

        logger = get_task_logger(__name__)
        for email_receiver in email_receivers:
            logger.info(f'Notification {notification_type} sending to {email_receiver}')
            send_email.delay('task claimed', email_receiver)
    #logger.info(f'Sending email')
    #send_mail(
    #    'Subject here',
    #    'Here is the message.',
    #   'from@example.com',
    #    ['mnunzio90@gmail.com'],
    #    fail_silently=False,
    #)
    #return x + y


@shared_task(queue='email', ignore_result=True)
def send_email(*args):
    logger = get_task_logger(__name__)
    logger.info(f'Email with message {args[0]} sending to {args[1]}')

