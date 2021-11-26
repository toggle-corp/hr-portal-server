import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from apps.leave.models import Leave, LeaveDay
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.types import CustomDjangoListObjectType
from .enums import LeaveTypeEnum, LeaveStatusEnum, LeaveDayTypeEnum
from utils.graphene.enums import EnumDescription


# def get_leave_qs(info):
#     return Leave.objects.filter(created_by=info.context.user)

class LeaveType(DjangoObjectType):
    class Meta:
        model = Leave
        fields = (
            'id', 'created_by', 'start_date', 'end_date',
            'num_of_days', 'additional_information',
            'denied_reason', 'created_at', 'leave_day'
        )
    type = graphene.Field(LeaveTypeEnum, required=True)
    type_display = EnumDescription(source='get_type_display', required=True)
    status = graphene.Field(LeaveStatusEnum, required=True)
    status_display = EnumDescription(source='get_status_display', required=True)

    # @staticmethod
    # def get_custom_queryset(root, info):
    #     return get_leave_qs(info)


class LeaveDayType(DjangoObjectType):
    class Meta:
        model = LeaveDay
        fields = (
            'id', 'date', 'additional_information',
        )
    type = graphene.Field(LeaveDayTypeEnum, required=True)
    type_display = EnumDescription(source='get_type_display', required=True)


class LeaveListType(CustomDjangoListObjectType):
    class Meta:
        model = Leave
        fields = (
            'id', 'created_by', 'start_date', 'end_date',
            'num_of_days', 'additional_information',
            'denied_reason', 'created_at', 'leave_day'
        )


class LeaveDayListType(CustomDjangoListObjectType):
    class Meta:
        model = LeaveDay
        fields = (
            'id', 'date', 'additional_information',
        )


class Query:
    leaves = DjangoPaginatedListObjectField(
        LeaveListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    leave_by_id = DjangoObjectField(LeaveType)
    leave_day = DjangoPaginatedListObjectField(
        LeaveDayListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    def resolve_leave_day(root, info, **kwargs):
        return LeaveDay.objects.select_related("leave").filter(leave__created_by=info.context.user)

    def resolve_leaves(root, info, **kwargs):
        # return get_leave_qs(info)
        return Leave.objects.filter(created_by=info.context.user)

    def resolve_leave_by_id(root, info, id):
        # Querying a single leave
        return Leave.objects.get(pk=id)
