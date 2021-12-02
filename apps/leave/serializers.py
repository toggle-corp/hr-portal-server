from rest_framework import serializers

from .models import Leave, LeaveDay


class LeaveDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveDay
        fields = ('additional_information, date, type')


class LeaveApplySerializer(serializers.ModelSerializer):
    # leave_days = LeaveDaySerializer(many=True)

    class Meta:
        model = Leave
        fields = ('start_date', 'end_date', 'status', 'additional_information',
                  'denied_reason', 'leave_days',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        leave_days = validated_data.pop('leave_days')
        leave = Leave.objects.create(**validated_data)
        for leave_day in leave_days:
            LeaveDay.objects.create(leave=leave, **leave_day)
        return leave
