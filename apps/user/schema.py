from typing import Union
from apps.user.models import User
import graphene
from graphene_django import DjangoObjectType

from .enums import UserGenderEnum
from utils.graphene.enums import EnumDescription


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'primary_email', 'secondary_email',
            'address', 'primary_phone_number', 'secondary_phone_number', 'avatar', 'avatar_url',
            'joined_at', 'birthday', 'is_superuser'
        )
    gender = graphene.Field(UserGenderEnum, required=True)
    gender_display = EnumDescription(source='get_gender_display', required=True)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_me(root, info, **kwargs) -> Union[User, None]:
        if info.context.user.is_authenticated:
            return info.context.user
        return None
