import graphene

from utils.graphene.error_types import mutation_is_not_valid, CustomErrorType
from utils.graphene.mutation import generate_input_type_for_serializer

from .serializers import (
    LeaveApplySerializer,
)

LeaveApplyInputType = generate_input_type_for_serializer('LeaveApplyInputType', LeaveApplySerializer)


class LeaveApply(graphene.Mutation):
    class Arguments:
        data = LeaveApplyInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, data):
        serializer = LeaveApplySerializer(data=data, context={'request': info.context})
        if errors := mutation_is_not_valid(serializer):
            return LeaveApply(
                errors=errors,
                ok=False,
            )
        serializer.save()
        return LeaveApply(
            errors=None,
            ok=True
        )


class Mutation():
    leave_apply = LeaveApply.Field()
