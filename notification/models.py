from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class EventType(models.IntegerChoices):
        TASK_CLAIMED = 0, _('Task Claimed')
        TASK_COMMENT = 1, _('Task Comment')
        SUBMISSION_APPROVED = 2, _('Submission Approved')
        SUBMISSION_REJECTED = 3, _('Submission Rejected')

    class Type(models.IntegerChoices):
        EMAIL = 0
        SMS = 1

    event_type = models.IntegerField(choices=EventType.choices)
    message = models.CharField(max_length=1000)


class EmailNotification(Notification):
    title = models.CharField(max_length=400)
    template = models.CharField(max_length=4000)
