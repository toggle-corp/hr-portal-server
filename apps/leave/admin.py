from django.contrib import admin
from apps.leave.models import Leave, LeaveDay
# Register your models here.


class LeaveAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'start_date', 'end_date', 'num_of_days', 'additional_information', 'status')
    readonly_fields = ('num_of_days', 'start_date', 'end_date')


class LeaveDayAdmin(admin.ModelAdmin):
    list_display = ('leave', 'date', 'type')


admin.site.register(Leave, LeaveAdmin)
admin.site.register(LeaveDay, LeaveDayAdmin)
