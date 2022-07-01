import json
import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from matching.models import BountyClaim, BountyDeliveryAttempt
from .types import TaskClaimType, TaskDeliveryAttemptType
from .mutations import CreateTaskClaimMutation


class TaskClaimQuery(ObjectType):
    matches = graphene.List(TaskClaimType)
    match = graphene.Field(TaskClaimType, id=graphene.Int())

    def resolve_match(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return BountyClaim.objects.get(pk=id)

        return None

    def resolve_matches(self, info, query=None, **kwargs):
        qs = BountyClaim.objects.all()
        return qs


class TaskDeliveryAttemptQuery(ObjectType):
    attempts = graphene.List(TaskDeliveryAttemptType)
    attempt = graphene.Field(TaskDeliveryAttemptType, id=graphene.Int())

    def resolve_attempt(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return BountyDeliveryAttempt.objects.filter(kind=0, task_claim__task_id=id).last()

        return None

    def resolve_attempts(self, info, query=None, **kwargs):
        qs = BountyDeliveryAttempt.objects.all()
        return qs


class TaskClaimMutations(graphene.ObjectType):
    create_match = CreateTaskClaimMutation.Field()

