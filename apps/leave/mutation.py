import graphene

from utils.graphene.error_types import mutation_is_not_valid, CustomErrorType
from utils.graphene.mutation import generate_input_type_for_serializer

from .serializers import (
    LeaveApplySerializer,
    # LeaveDaySerializer
)
from .schema import LeaveType

LeaveApplyInputType = generate_input_type_for_serializer('LeaveApplyInputType', LeaveApplySerializer)
# LeaveDayInputType = generate_input_type_for_serializer('LeaveDayInputType', LeaveDaySerializer)


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


class Mutation():
    leave_apply = LeaveApply.Field()
