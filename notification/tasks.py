from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from notification.models import EmailNotification, Notification
from talent.models import Person


def _forward_notification(notification_types, event_type, params):
    if Notification.Type.EMAIL in notification_types:
        send_email.delay(event_type, **params)
    elif Notification.Type.SMS in notification_types:
        # TODO add task to send sms
        pass


def _build_notification_params(event_type, notification_params):
    params = notification_params.copy()
    if event_type == Notification.EventType.TASK_CLAIMED:
        pass
    elif event_type == Notification.EventType.SUBMISSION_APPROVED:
        pass
    return params


@shared_task(queue='notification', ignore_result=True)
def send_notification(notification_types, event_type, receivers, **kwargs):
    logger = get_task_logger(__name__)

    for receiver in receivers:
        logger.info(f'Notification {event_type} sending to {receiver}')
        params = _build_notification_params(event_type, kwargs)
        params['receiver'] = receiver
        _forward_notification(notification_types, event_type, params)


@shared_task(queue='email', ignore_result=True)
def send_email(event_type, **kwargs):
    logger = get_task_logger(__name__)

    email_receiver = Person.objects.values_list('email_address', flat=True).distinct('email_address').filter(
        id=kwargs['receiver']).get()
    email_notification = EmailNotification.objects.filter(event_type=event_type).get()

    email_title = email_notification.title.format(**kwargs)
    notification_message = email_notification.message.format(**kwargs)
    email_content = email_notification.template.format(message=notification_message)

    logger.info(f'Email with title {email_title} and message {email_content} sending to {email_receiver}')
    send_mail(
        email_title,
        email_content,
        'test@example.com',
        [email_receiver]
    )
