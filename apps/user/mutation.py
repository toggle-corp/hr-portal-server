import graphene

from django.contrib.auth import login, logout

from utils.graphene.error_types import mutation_is_not_valid, CustomErrorType
from utils.graphene.mutation import generate_input_type_for_serializer
from .serializers import (
    LoginSerializer,
)
from .schema import UserType


LoginInputType = generate_input_type_for_serializer('LoginInputType', LoginSerializer)


class Login(graphene.Mutation):
    class Arguments:
        data = LoginInputType(required=True)

    result = graphene.Field(UserType)
    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, data):
        serializer = LoginSerializer(data=data, context={'request': info.context})
        if errors := mutation_is_not_valid(serializer):
            return Login(
                errors=errors,
                ok=False,
            )

        if user := serializer.validated_data.get('user'):
            login(info.context, user)
        return Login(
            result=user,
            errors=None,
            ok=True
        )


class Logout(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self, info, *args, **kwargs):
        if info.context.user.is_authenticated:
            logout(info.context)
        return Logout(ok=True)


class Mutation():
    login = Login.Field()
    logout = Logout.Field()
