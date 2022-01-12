from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker
from notifications.signals import notify

from backend.utils import send_email
from work.models import Task
from talent.models import Person
from backend.mixins import TimeStampMixin, UUIDMixin

CLAIM_TYPE_DONE = 0
CLAIM_TYPE_ACTIVE = 1
CLAIM_TYPE_FAILED = 2
CLAIM_TYPE_IN_REVIEW = 3


class TaskClaim(TimeStampMixin, UUIDMixin):
    CLAIM_TYPE = (
        (CLAIM_TYPE_DONE, "Done"),
        (CLAIM_TYPE_ACTIVE, "Active"),
        (CLAIM_TYPE_FAILED, "Failed"),
        (CLAIM_TYPE_IN_REVIEW, "In review")
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    kind = models.IntegerField(choices=CLAIM_TYPE, default=0)
    tracker = FieldTracker()

    def __str__(self):
        return '{}: {} ({})'.format(self.task, self.person, self.kind)


@receiver(post_save, sender=TaskClaim)
def save_task_claim(sender, instance, created, **kwargs):
    task = instance.task
    reviewer = getattr(task, "reviewer", None)
    contributor = instance.person
    contributor_email = contributor.email_address
    reviewer_user = reviewer.user if reviewer else None

    if not created:
        # contributor quits the task
        if instance.kind == CLAIM_TYPE_FAILED and instance.tracker.previous("kind") is not CLAIM_TYPE_FAILED:
            subject = "The contributor quits the task"
            message = f"The contributor quits the task: {task.get_task_link()}"
            if reviewer:
                notify.send(instance, recipient=reviewer_user, verb=subject, description=message)
                send_email(
                    to_emails=reviewer.email_address,
                    subject=subject,
                    content=message
                )

            # subject = "The admin cancel the claim"
            # message = "The admin cancel the task claim"
            # notify.send(instance, recipient=contributor.user, verb=subject, description=message)
            # send_email(
            #     to_emails=contributor_email,
            #     subject=subject,
            #     content=message
            # )

        # contributor submit the work for review
        if instance.kind == CLAIM_TYPE_DONE and instance.tracker.previous("kind") is not CLAIM_TYPE_DONE:
            task = instance.task
            subject = f"The task \"{task.title}\" is ready to review"
            message = f"You can see the task here: {task.get_task_link()}"
            if reviewer:
                notify.send(instance, recipient=reviewer_user, verb=subject, description=message)
                send_email(
                    to_emails=reviewer.email_address,
                    subject=subject,
                    content=message
                )


class TaskDeliveryAttempt(TimeStampMixin):
    CLAIM_REQUEST_TYPE = (
        (0, "New"),
        (1, "Approved"),
        (2, "Rejected"),
    )
    kind = models.IntegerField(choices=CLAIM_REQUEST_TYPE, default=0)
    task_claim = models.ForeignKey(TaskClaim, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name="delivery_messages")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    is_canceled = models.BooleanField(default=False)
    delivery_message = models.CharField(max_length=2000, default=None)
    tracker = FieldTracker()


class TaskDeliveryAttachment(models.Model):
    task_delivery_attempt = models.ForeignKey(TaskDeliveryAttempt, on_delete=models.CASCADE, related_name='attachments')
    file_type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)


@receiver(post_save, sender=TaskDeliveryAttempt)
def save_task_claim_request(sender, instance, created, **kwargs):
    task_claim = instance.task_claim
    contributor = instance.person
    contributor_email = contributor.email_address
    reviewer = getattr(task_claim, "reviewer", None)
    reviewer_user = reviewer.user if reviewer else None

    # contributor request to claim it
    if created and not task_claim.task.auto_approve_task_claims:
        subject = f"A new task delivery attempt has been created"
        message = f"A new task delivery attempt has been created for the \"{task_claim.task.title}\" task"

        if reviewer:
            notify.send(instance, recipient=reviewer_user, verb=subject, description=message)
            send_email(
                to_emails=reviewer.email_address,
                subject=subject,
                content=message
            )

    if not created:
        # contributor cancel the claim request
        if instance.tracker.previous("kind") == 0 and instance.kind == 1:
            subject = f"The task claim request has been canceled"
            message = f"The task claim request has been canceled for the \"{task_claim.task.title}\" task"

            if reviewer:
                notify.send(instance, recipient=reviewer_user, verb=subject, description=message)

            notify.send(instance, recipient=contributor.user, verb=subject, description=message)

            send_email(
                to_emails=[contributor_email, reviewer.email_address],
                subject=subject,
                content=message
            )

        # contributor cancel the claim request
        if instance.tracker.previous("kind") == 0 and instance.kind == 2:
            subject = f"The task claim request has been rejected"
            message = f"The task claim request has been rejected for the \"{task_claim.task.title}\" task"

            notify.send(instance, recipient=contributor.user, verb=subject, description=message)

            send_email(
                to_emails=contributor_email,
                subject=subject,
                content=message
            )

        # admin accept the request
        if instance.kind == 0 and instance.tracker.previous("kind") != 0:
            subject = f"A new task claim request has been approved"
            message = f"A new task claim request has been approved for the \"{task_claim.task.title}\" task"

            notify.send(instance, recipient=contributor.user, verb=subject, description=message)
            send_email(
                to_emails=contributor_email,
                subject=subject,
                content=message
            )

        # contributor quits the task
        if instance.is_canceled and not instance.tracker.previous("is_canceled"):
            subject = f"The contributor leave the task"
            message = f"The contributor leave the task \"{task_claim.task.title}\""

            if reviewer:
                notify.send(instance, recipient=reviewer_user, verb=subject, description=message)
                send_email(
                    to_emails=reviewer.email_address,
                    subject=subject,
                    content=message
                )
        if task_claim.kind == CLAIM_TYPE_IN_REVIEW:
            task_claim.delete()
