from django.db import models
from django.utils.translation import gettext_lazy as _

from hr_portal.models import UserResourceModel
from apps.user.models import User


class Leave(UserResourceModel):
    class Type(models.IntegerChoices):
        SICK = 0, _('Sick leave (Illness or Injury)')
        PERSONAL_OR_CASUAL = 1, _('Personal/Casual')
        BEREAVEMENT_IMMEDIATE_FAMILY = 2, _('Bereavement leave (Immediate Family)')
        BEREAVEMENT_OTHER = 3, _('Bereavement leave (Other)')
        JURY_DUTY_LEGAL = 4, _('Jury duty or legal')
        EMERGENCY = 5, _('Emergency')
        UNPAID = 6, _('Unpaid')
        TC_GRANTED = 7, _('TC Granted')
        COVID = 8, _('COVID')
        REPLACEMENT = 9, _('Replacement')
        MATERNITY = 10, _('Maternity')
        PATERNITY = 11, _('Paternity')
        MENSTRUAL = 12, _('Menstrual')
        OTHER = 13, _('Other')

    class Status(models.IntegerChoices):
        PENDING = 0, _('Pending')
        APPROVED = 1, _('Approved')
        DENIED = 2, _('Denied')

    type = models.IntegerField(choices=Type.choices)
    status = models.IntegerField(
        choices=Status.choices, default=Status.APPROVED
    )
    num_of_days = models.FloatField(verbose_name='number of days(Auto-calculated)', blank=True)
    start_date = models.DateField(null=True, verbose_name='start date(Auto-calculated)')
    end_date = models.DateField(null=True, verbose_name='end date(Auto-calculated)')
    additional_information = models.TextField(null=True, blank=True)
    denied_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.created_by} # {self.id}'


class LeaveDay(models.Model):
    class Type(models.IntegerChoices):
        FIRST_HALF = 0, _('First half')
        SECOND_HALF = 1, _('Second half')
        FULL = 2, _('Full')
        NO_LEAVE = 3, _('No Leave')

    leave = models.ForeignKey(Leave, on_delete=models.CASCADE, related_name="leave_days")
    date = models.DateField()
    type = models.IntegerField(choices=Type.choices, default=Type.FULL)
    additional_information = models.TextField(blank=True)

    def __str__(self):
        return str(self.date)
