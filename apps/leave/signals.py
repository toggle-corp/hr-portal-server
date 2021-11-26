from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

from .models import Leave, LeaveDay


@receiver(post_save, sender=Leave)
def create_leave_days(sender, instance, created, *args, **kwargs):
    """
    Created leave_day on creating any new leave.
    """
    if created:

        delta = instance.end_date - instance.start_date
        days = []
        for i in range(delta.days + 1):
            day = instance.start_date + timedelta(days=i)
            days.append(day)

        for day in days:
            LeaveDay.objects.create(leave=instance, date=day)
