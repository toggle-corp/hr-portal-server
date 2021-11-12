from apps.user.models import User
import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'gender', 'primary_email',
            'address', 'primary_phone_number'
        )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        print(info.context.user.is_authenticated)
        return User.objects.all()
