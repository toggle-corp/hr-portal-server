from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings

from hr_portal.mail import send_mail

from .models import Leave

DEFAULT_CC_EMAILS = [settings.MANAGEMENT_EMAIL, settings.HR_EMAIL]


def _send_leave_email(leave, *email_template_args):
    context = {
        'leave': leave,
    }
    departments = leave.created_by.user_department.all()
    cc = [*DEFAULT_CC_EMAILS]
    if departments:
        for department in departments:
            cc += [f'{department.department.name} <{department.department.email}>']
    transaction.on_commit(
        lambda: send_mail(
            leave.created_by,
            context,
            *email_template_args,
            cc=cc,
            reply_to=[settings.HR_EMAIL],
        )
    )


APPROVED_EMAIL_TEMPLATES_ARGS = [
    'email/leave/subject.txt',
    'email/leave/noted/body.txt',
    'email/leave/noted/body.html',
]

DENIED_EMAIL_TEMPLATES_ARGS = [
    'email/leave/subject.txt',
    'email/leave/denied/body.txt',
    'email/leave/denied/body.html',
]


@receiver(post_save, sender=Leave)
def send_email_notifications_when_leave_created(sender, instance, created, **kwargs):
    if instance.status == Leave.Status.DENIED:
        _send_leave_email(instance, *DENIED_EMAIL_TEMPLATES_ARGS)
    elif instance.status == Leave.Status.APPROVED:
        _send_leave_email(instance, *APPROVED_EMAIL_TEMPLATES_ARGS)
