# -*- coding: utf-8 -*-
from django.core.management import BaseCommand

from notification.models import EmailNotification, Notification
from work.models import *


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def create_notification(self):
        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.TASK_CLAIMED,
            permitted_params='task_id,user',
            title='Claim of task {task_id}',
            template='The task {task_id} is claimed by {user}'
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.SUBMISSION_APPROVED,
            permitted_params='task_id,user',
            title='Approving task {task_id}',
            template='The task {task_id} is approved'
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.BUG_REJECTED,
            permitted_params='headline,link,product,description',
            title='The bug was rejected',
            template='''<p>The <strong>&laquo;{headline}&raquo;</strong> bug for product <strong>&laquo;{product}&raquo;</strong> was rejected.</p>
                        <p>Explanation of the decision:</p>
                        <blockquote>{description}</blockquote>'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.IDEA_REJECTED,
            permitted_params='headline,link,product,description',
            title='The idea was rejected',
            template='''<p>The <strong>&laquo;{headline}&raquo;</strong> idea for product <strong>&laquo;{product}&raquo;</strong> was rejected.</p>
                        <p>Explanation of the decision:</p>
                        <blockquote>{description}</blockquote>'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.BUG_CREATED,
            permitted_params='headline,link,product',
            title='New bug successfully created',
            template='''The <strong>&laquo;{headline}&raquo;</strong> bug for product <strong>&laquo;{product}&raquo;</strong> is successfully created.
                        You can see the bug here: <a href="{link}" target="_blank">{link}</a>'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.IDEA_CREATED,
            permitted_params='headline,link,product',
            title='New idea successfully created',
            template='''The <strong>&laquo;{headline}&raquo;</strong> idea for product <strong>&laquo;{product}&raquo;</strong> is successfully created.
                        You can see the idea here: <a href="{link}" target="_blank">{link}</a>'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.BUG_CREATED_FOR_MEMBERS,
            permitted_params='headline,link,product',
            title='New bug for {product} was created',
            template='''The <strong>&laquo;{headline}&raquo;</strong> bug for product <strong>&laquo;{product}&raquo;</strong> was created.
                        The bug is available here: <a href="{link}" target="_blank">{link}</a>'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.IDEA_CREATED_FOR_MEMBERS,
            permitted_params='headline,link,product',
            title='New idea for {product} was created',
            template='''The <strong>&laquo;{headline}&raquo;</strong> idea for product <strong>&laquo;{product}&raquo;</strong> was created.
                        The idea is available here: <a href="{link}" target="_blank">{link}</a>'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.TASK_STATUS_CHANGED,
            permitted_params='title,link',
            title='Task status changed',
            template='''The task {title} is claimed now.
                    You can see the task here: {link}'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.TASK_IN_REVIEW,
            permitted_params='title,link',
            title='The task status was changed to "In review"',
            template='''The task {title} status was changed to "In review".
                        You can see the task here: {link}'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.GENERIC_COMMENT,
            permitted_params='text',
            title='You have been mentioned in the comment',
            template='''{text}'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.TASK_SUBMITTED,
            permitted_params='task_title,task_link,person_first_name',
            title='Task has been submitted',
            template='''The task {task_title} has been submitted by {person_first_name}.
                        You can see the task here: {task_link}'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.TASK_READY_TO_REVIEW,
            permitted_params='task_title,task_link',
            title='The task "{task_title}" is ready to review',
            template='''You can see the task here: {task_link}'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.TASK_DELIVERY_ATTEMPT_CREATED,
            permitted_params='task_title',
            title='A new task delivery attempt has been created',
            template='''A new task delivery attempt has been created for the "{task_title}" task'''
        )

        EmailNotification.objects.get_or_create(
            event_type=Notification.EventType.CONTRIBUTOR_LEFT_TASK,
            permitted_params='task_title',
            title='The contributor leave the task',
            template=''' The contributor leave the task "{task_title}"'''
        )

    def handle(self, *args, **options):
        # Create notification
        self.create_notification()
