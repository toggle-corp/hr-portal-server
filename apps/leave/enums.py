from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import Leave, LeaveDay

LeaveTypeEnum = convert_enum_to_graphene_enum(Leave.Type, name='LeaveTypeEnum')
LeaveStatusEnum = convert_enum_to_graphene_enum(Leave.Status, name='LeaveStatusEnum')
LeaveDayTypeEnum = convert_enum_to_graphene_enum(LeaveDay.Type, name='LeaveDayTypeEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (Leave.type, LeaveTypeEnum),
        (Leave.status, LeaveStatusEnum),
        (LeaveDay.type, LeaveDayTypeEnum)
    )
}
