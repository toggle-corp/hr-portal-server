import graphene
from django.utils.translation import gettext
from django.core.exceptions import ObjectDoesNotExist

from utils.graphene.error_types import mutation_is_not_valid, CustomErrorType
from utils.graphene.mutation import generate_input_type_for_serializer

from .serializers import (
    LeaveApplySerializer,
    LeaveUpdateSerializer
)
from .schema import LeaveType
from .models import Leave

LeaveApplyInputType = generate_input_type_for_serializer('LeaveApplyInputType', LeaveApplySerializer)
LeaveUpdateInputType = generate_input_type_for_serializer('LeaveUpdateInputType', LeaveUpdateSerializer)


class LeaveApply(graphene.Mutation):

    class Arguments:
        data = LeaveApplyInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean(required=True)
    result = graphene.Field(LeaveType)

    @staticmethod
    def mutate(root, info, data):
        serializer = LeaveApplySerializer(data=data, context={'request': info.context})
        if errors := mutation_is_not_valid(serializer):
            return LeaveApply(
                errors=errors,
                ok=False,
            )
        instance = serializer.save()

        return LeaveApply(
            errors=None,
            ok=True,
            result=instance,
        )


class LeaveUpdate(graphene.Mutation):
    class Arguments:
        data = LeaveUpdateInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(LeaveType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Leave.objects.get(id=data['id'])
        except ObjectDoesNotExist:
            return LeaveUpdate(errors=[
                dict(field='nonFieldErrors', messages=gettext('Leave does not exist.'))
            ])
        serializer = LeaveUpdateSerializer(
            instance=instance,
            data=data,
            context={'request': info.context},
            partial=True
        )
        if errors := mutation_is_not_valid(serializer):
            return LeaveUpdate(errors=errors, ok=False)
        serializer.save()
        return LeaveUpdate(result=serializer.instance, errors=None, ok=True)


class Mutation():
    leave_apply = LeaveApply.Field()
    leave_update = LeaveUpdate.Field()
