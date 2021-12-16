from typing import Union
import graphene
from django.db.models import Sum
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination

from .enums import UserGenderEnum
from utils.graphene.enums import EnumDescription
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.types import CustomDjangoListObjectType
from .filters import UserFilterSet
from apps.leave.models import Leave
from apps.user.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'primary_email', 'secondary_email',
            'address', 'primary_phone_number', 'secondary_phone_number', 'joined_at', 'birthday'
        )
        filterset_class = UserFilterSet

    gender = graphene.Field(UserGenderEnum, required=True)
    gender_display = EnumDescription(source='get_gender_display', required=True)
    remaining_leave = graphene.String()
    total_leaves_days = graphene.String()

    @staticmethod
    def resolve_remaining_leave(root, info, **kwargs) -> Union[str, None]:
        user = info.context.user
        user_leaves = Leave.objects.filter(
            status=Leave.Status.APPROVED,
            created_by=info.context.user).exclude(
                type=Leave.Type.UNPAID).aggregate(Sum('num_of_days'))
        if user_leaves['num_of_days__sum']:
            remaining_leave = user.total_leaves_days - float(user_leaves['num_of_days__sum'])
        else:
            remaining_leave = user.total_leaves_days
        return remaining_leave

    @staticmethod
    def resolve_total_leave_days(root, info, **kwargs) -> Union[str, None]:
        user = info.context.user
        return user.total_leaves_days


class UserListType(CustomDjangoListObjectType):
    class Meta:
        model = User
        filterset_class = UserFilterSet


class UserMeType(DjangoObjectType):
    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id', 'first_name', 'last_name', 'is_active',
            'email', 'last_login',

        )
    gender = graphene.Field(UserGenderEnum, required=True)
    gender_display = EnumDescription(source='get_gender_display', required=True)


class Query:
    users = DjangoPaginatedListObjectField(
        UserListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    me = graphene.Field(UserMeType)

    def resolve_me(root, info, **kwargs) -> Union[User, None]:
        if info.context.user.is_authenticated:
            return info.context.user
        return None
