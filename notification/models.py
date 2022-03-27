from django.core.exceptions import ValidationError
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

    event_type = models.IntegerField(choices=EventType.choices, primary_key=True)
    permitted_params = models.CharField(max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_event_type_display()


class EmailNotification(Notification):
    title = models.CharField(max_length=400)
    template = models.CharField(max_length=4000)

    def clean(self):
        _template_is_valid(self.title, self.permitted_params)
        _template_is_valid(self.template, self.permitted_params)


def _template_is_valid(template, permitted_params):
    permitted_params_list = permitted_params.split(',')
    params = {param: '' for param in permitted_params_list}
    try:
        template.format(**params)
    except IndexError:
        raise ValidationError({'template': _('No curly brace without a name permitted')}) from None
    except KeyError as ke:
        raise ValidationError({'template': _(f"{ke.args[0]} isn't a permitted param for template. Please use one of these: {permitted_params}")}) from None