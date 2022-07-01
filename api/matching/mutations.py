import graphene

import notification.tasks
from matching.models import BountyClaim
from notification.models import Notification
from talent.models import Person
from work.models import Challenge
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
            challenge = Challenge.objects.get(id=input.task)
            person = Person.objects.get(id=input.person)
            match = BountyClaim(challenge=challenge, person=person, kind=input.kind)
            match.save()
            status = True

            if challenge.reviewer:
                notification.tasks.send_notification.delay([Notification.Type.EMAIL],
                                                           Notification.EventType.TASK_SUBMITTED,
                                                           receivers=[challenge.reviewer.id],
                                                           task_title=challenge.title,
                                                           task_link=challenge.get_challenge_link(),
                                                           person_first_name=person.first_name)
        except:
            pass

        return CreateTaskClaimMutation(match=match, status=status)
