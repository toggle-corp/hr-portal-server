from apps.leave.models import Leave, LeaveDay
import graphene
from graphene_django import DjangoObjectType
from .enums import LeaveTypeEnum, LeaveStatusEnum, LeaveDayTypeEnum
from utils.graphene.enums import EnumDescription


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


class LeaveDayType(DjangoObjectType):
    class Meta:
        model = LeaveDay
        fields = (
            'id', 'date', 'additional_information',
        )
    type = graphene.Field(LeaveDayTypeEnum, required=True)
    type_display = EnumDescription(source='get_type_display', required=True)


class Query(graphene.ObjectType):
    leaves = graphene.List(LeaveType)
    leave_by_id = graphene.Field(LeaveType, id=graphene.String())
    leave_day = graphene.List(LeaveDayType)

    def resolve_leave_day(root, info):
        return LeaveDay.objects.select_related("leave").filter(created_by=info.context.user)

    def resolve_leaves(root, info):
        return Leave.objects.filter(created_by=info.context.user)

    def resolve_leave_by_id(root, info, id):
        # Querying a single leave
        return Leave.objects.get(pk=id)
