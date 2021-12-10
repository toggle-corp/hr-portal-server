from rest_framework import serializers
from django.db import transaction
from django.db.models import Sum

from .models import Leave, LeaveDay
from hr_portal.serializers import UpdateSerializerMixin, MetaInformationSerializerMixin


class IntegerIDField(serializers.IntegerField):
    """
    This field is created to override the graphene conversion of the integerfield
    """
    pass


class LeaveDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveDay
        exclude = ['id', 'leave']


class LeaveDayUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = LeaveDay
        exclude = ['leave']


class LeaveApplySerializer(MetaInformationSerializerMixin, serializers.ModelSerializer):
    leave_days = LeaveDaySerializer(many=True)

    class Meta:
        model = Leave
        fields = (
            'additional_information',
            'type',
            'leave_days'
        )

    def validate(self, attrs):
        user = self.context['request'].user

        # check for already applied leave
        date_list = [leave_day['date'] for leave_day in attrs['leave_days']]
        existed_leave_days = LeaveDay.objects.filter(
            date__in=date_list,
            leave__created_by=user).values_list(
                'date', flat=True)
        if existed_leave_days:
            existed_leave_day_dates = [str(leave_day) for leave_day in existed_leave_days]
            raise serializers.ValidationError({
                "date": 'Leave already exists : {}'.format(', '.join(existed_leave_day_dates))
            })

        # check if numbr of paid leave days is over
        if not attrs['type'] == 6:
            user_leaves = Leave.objects.filter(
                status=1,
                created_by=user).exclude(
                    type=6).aggregate(Sum('num_of_days'))
            if user_leaves['num_of_days__sum']:
                # TODO :Need to adjust total sum incase of other not countable leaves.
                if user_leaves['num_of_days__sum'] >= user.total_leaves_days:
                    raise serializers.ValidationError({
                        "date": "Total number of paid leave is over, Please apply unpaid leave",
                    })

        return attrs

    @staticmethod
    def get_num_of_days(leave_days):
        num_of_days = 0
        for leave_day in leave_days:
            if leave_day['type'] == 3:
                num_of_days += 0
            elif leave_day['type'] == 2:
                num_of_days += 1
            else:
                num_of_days += 0.5
        return num_of_days

    @staticmethod
    def remove_weekdays(leave_days):
        removed_weekday_list = []
        for leave_day in leave_days:
            if not (leave_day['date'].weekday() == 5 or leave_day['date'].weekday() == 6):
                removed_weekday_list.append(leave_day)
        return removed_weekday_list

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        leave_days = self.remove_weekdays(validated_data.pop('leave_days'))
        validated_data['start_date'] = leave_days[0]['date']
        validated_data['end_date'] = leave_days[-1]['date']
        validated_data['num_of_days'] = self.get_num_of_days(leave_days)
        leave = Leave.objects.create(**validated_data)
        for leave_day in leave_days:
            if leave_day['type'] == 3:
                continue
            LeaveDay.objects.create(leave=leave, **leave_day)
        return leave

    @transaction.atomic
    def update(self, instance, validated_data):
        leave_days = self.remove_weekdays(validated_data.pop('leave_days'))
        validated_data['start_date'] = leave_days[0]['date']
        validated_data['end_date'] = leave_days[-1]['date']
        validated_data['num_of_days'] = self.get_num_of_days(leave_days)
        instance = super().update(instance, validated_data)

        for leave_day in leave_days:
            leave_day_id = leave_day.get('id', None)
            if leave_day_id:
                leave_day_instance = LeaveDay.objects.get(id=leave_day_id, leave=instance)
                leave_day_instance.additional_information = leave_day.get(
                    'additional_information',
                    leave_day_instance.additional_information)
                leave_day_instance.date = leave_day.get('date', leave_day_instance.date)
                leave_day_instance.type = leave_day.get('type', leave_day_instance.type)
                leave_day_instance.save()
            else:
                leave_day = LeaveDay.objects.create(leave=instance, **leave_day)

        return instance


class LeaveUpdateSerializer(UpdateSerializerMixin, LeaveApplySerializer):
    leave_days = LeaveDayUpdateSerializer(many=True)
    id = IntegerIDField(required=True)

    class Meta:
        model = Leave
        fields = (
            'id',
            'additional_information',
            'type',
            'leave_days'
        )

    def validate(self, attrs):
        user = self.context['request'].user
        leave_days = self.remove_weekdays(attrs.pop('leave_days'))

        # check if leave status is approved or denied
        date_list = [leave_day['date'] for leave_day in leave_days]
        current_leave_days = LeaveDay.objects.filter(leave=self.instance).values_list('date', flat=True)
        current_leave_status = self.instance.status
        if current_leave_status in [1, 2]:
            raise serializers.ValidationError({
                'date': 'You cannot update this leave request'
            })

        # check for already applied leave for additional days
        existed_leave_days = LeaveDay.objects.filter(
            leave__created_by=user,
            date__in=date_list).exclude(
                date__in=current_leave_days).values_list(
                    'date', flat=True)
        if existed_leave_days:
            existed_leave_days = [str(leave_day) for leave_day in existed_leave_days]
            raise serializers.ValidationError({
                'date': 'leave_exists : {}'.format(', '.join(existed_leave_days))
            })

        # check if numbr of paid leave days is over
        if not attrs['type'] == 6:
            total_number_of_days_applied = Leave.objects.filter(
                status=1,
                created_by=user).exclude(type=6).aggregate(Sum('num_of_days'))
            # TODO :Need to adjust total sum incase of other not countable leaves.
            if (total_number_of_days_applied['num_of_days__sum'] >= user.total_leaves_days):
                raise serializers.ValidationError({
                    'date': "Total number of paid leave is over, Please apply unpaid leave"
                })
            if (total_number_of_days_applied['num_of_days__sum'] + self.get_num_of_days(leave_days)) \
                    > user.total_leaves_days:
                raise serializers.ValidationError({
                    "date": "Number of leave days applied exceeds total number of leave days allocated "
                })

        return attrs
