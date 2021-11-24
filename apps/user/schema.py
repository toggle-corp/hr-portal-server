from typing import Union
from apps.user.models import User
import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination

from .enums import UserGenderEnum
from utils.graphene.enums import EnumDescription
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.types import CustomDjangoListObjectType
from .filters import UserFilterSet


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'primary_email', 'secondary_email',
            'address', 'primary_phone_number', 'secondary_phone_number', 'joined_at', 'birthday'
        )
        filterset_class = UserFilterSet

    gender = graphene.Field(UserGenderEnum, required=True)
    gender_display = EnumDescription(source='get_gender_display', required=True)


# class UserListType(CustomDjangoListObjectType):
#     class Meta:
#         model = User
#         filterset_class = UserFilterSet


class UserMeType(DjangoObjectType):
    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id', 'first_name', 'last_name', 'is_active',
            'email', 'last_login',
        )


class Query:
    # users = DjangoPaginatedListObjectField(
    #     UserListType,
    #     pagination=PageGraphqlPagination(
    #         page_size_query_param='pageSize'
    #     )
    # )
    me = graphene.Field(UserMeType)

    def resolve_me(root, info, **kwargs) -> Union[User, None]:
        if info.context.user.is_authenticated:
            return info.context.user
        return None
