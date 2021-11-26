import graphene
from typing import Union
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from apps.leave.models import Leave, LeaveDay
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.types import CustomDjangoListObjectType
from .enums import LeaveTypeEnum, LeaveStatusEnum, LeaveDayTypeEnum
from utils.graphene.enums import EnumDescription


# def get_leave_qs(info):
#     return Leave.objects.filter(created_by=info.context.user)
DAYS_TYPE = {
    "ONE_DAY": "One Day",
    "MULTIPLE_DAY": "Multiple Days"
}


class LeaveDayType(DjangoObjectType):
    class Meta:
        model = LeaveDay
        fields = (
            'id', 'date', 'additional_information',
        )
    type = graphene.Field(LeaveDayTypeEnum, required=True)
    type_display = EnumDescription(source='get_type_display', required=True)


class LeaveType(DjangoObjectType):
    class Meta:
        model = Leave
        fields = (
            'id', 'created_by', 'start_date', 'end_date',
            'num_of_days', 'additional_information',
            'denied_reason', 'created_at'
        )
    type = graphene.Field(LeaveTypeEnum, required=True)
    type_display = EnumDescription(source='get_type_display', required=True)
    status = graphene.Field(LeaveStatusEnum, required=True)
    status_display = EnumDescription(source='get_status_display', required=True)
    leave_day = graphene.List(LeaveDayType, required=True)
    request_day_type = graphene.String()

    def resolve_leave_day(root, info, **kwargs) -> Union[str, None]:
        return LeaveDay.objects.select_related("leave").filter(leave=root)

    def resolve_request_day_type(root, info, **kwargs) -> Union[str, None]:
        return DAYS_TYPE["MULTIPLE_DAY"]
    # @staticmethod
    # def get_custom_queryset(root, info):
    #     return get_leave_qs(info)


class LeaveListType(CustomDjangoListObjectType):
    class Meta:
        model = Leave
        filterset_class = []


class Query:
    leaves = DjangoPaginatedListObjectField(
        LeaveListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    leave = DjangoObjectField(LeaveType)

    def resolve_leaves(root, info, **kwargs):
        # return get_leave_qs(info)
        return Leave.objects.filter(created_by=info.context.user)

    def resolve_leave(root, info, id):
        # Querying a single leave
        return Leave.objects.get(pk=id)
