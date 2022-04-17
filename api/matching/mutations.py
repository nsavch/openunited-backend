import graphene

import notification.tasks
from matching.models import TaskClaim
from notification.models import Notification
from talent.models import Person
from work.models import Task
from .types import TaskClaimInput, TaskClaimType


class CreateTaskClaimMutation(graphene.Mutation):
    class Arguments:
        input = TaskClaimInput(
            required=True,
            description=("Fields required to create a product"),
        )

    match = graphene.Field(TaskClaimType)
    status = graphene.Boolean()

    @staticmethod
    def mutate(*args, **kwargs):
        input = kwargs.get('input')
        status = False
        match = None

        try:
            task = Task.objects.get(id=input.task)
            person = Person.objects.get(id=input.person)
            match = TaskClaim(task=task, person=person, kind=input.kind)
            match.save()
            status = True

            if task.reviewer:
                notification.tasks.send_notification.delay([Notification.Type.EMAIL],
                                                           Notification.EventType.TASK_SUBMITTED,
                                                           receivers=[task.reviewer.id],
                                                           task_title=task.title,
                                                           task_link=task.get_task_link(),
                                                           person_first_name=person.first_name)
        except:
            pass

        return CreateTaskClaimMutation(match=match, status=status)
