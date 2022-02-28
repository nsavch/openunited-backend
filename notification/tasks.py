from celery import shared_task
from celery.utils.log import get_task_logger
#from django.core.mail import send_mail
from notification.models import EmailNotification, NOTIFICATION_TYPE_CLAIM
from talent.models import Person


@shared_task(queue='notification', ignore_result=True)
def send_notification(notification_type, **kwargs):
    logger = get_task_logger(__name__)

    if notification_type == NOTIFICATION_TYPE_CLAIM:
        params = kwargs.copy()
        del params['receivers']
        for receiver in kwargs['receivers']:
            logger.info(f'Notification {notification_type} sending to {receiver}')
            params['receiver'] = receiver
            send_email.delay(notification_type, **params)


@shared_task(queue='email', ignore_result=True)
def send_email(notification_type, **kwargs):
    logger = get_task_logger(__name__)

    email_receiver = Person.objects.values_list('email_address', flat=True).distinct('email_address').filter(
        id=kwargs['receiver']).get()
    email_notification = EmailNotification.objects.filter(type=notification_type).get()

    email_title = email_notification.title.format(**kwargs)
    notification_message = email_notification.message.format(**kwargs)
    email_content = email_notification.template.format(message=notification_message)

    logger.info(f'Email with title {email_title} and message {email_content} sending to {email_receiver}')
    # send_mail(
    #    email_title,
    #    email_content,
    #    [args[1]],
    # )