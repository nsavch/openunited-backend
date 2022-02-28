from django.db import models

NOTIFICATION_TYPE_CLAIM = 0
NOTIFICATION_TYPE_COMMENT = 1
NOTIFICATION_TYPE_APPROVE_TASK = 2


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        (NOTIFICATION_TYPE_CLAIM, "Claim"),
        (NOTIFICATION_TYPE_APPROVE_TASK, "Approve Task")
    )
    type = models.IntegerField(choices=NOTIFICATION_TYPE)
    message = models.CharField(max_length=1000)


class EmailNotification(Notification):
    title = models.CharField(max_length=400)
    template = models.CharField(max_length=4000)
