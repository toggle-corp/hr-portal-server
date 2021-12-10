import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


def _send_mail(
    subject_template_name,
    email_template_name_text,
    email_template_name_html,
    context, from_email, to,
    bcc=None, cc=None, reply_to=None,
):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    # Generate subject
    subject = render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())  # Email subject *must not* contain newlines
    # Generate body (text and html)
    text_content = render_to_string(email_template_name_text, context)
    html_content = render_to_string(email_template_name_html, context)
    # Create email object
    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Text
        from_email=from_email,
        to=[to],
        bcc=bcc,
        cc=cc,
        reply_to=reply_to,
    )
    email_message.attach_alternative(html_content, "text/html")
    # Send email
    email_message.send()


def send_mail(
    user,
    context,
    subject_template_name,
    email_template_name_text,
    email_template_name_html,
    **kwargs,
):
    """
    Validates email request
    Add common context variable
    """
    if not user.is_active:
        logger.warning(f'Email not sent: User <{user.email}>({user.pk}) is not active !!')
        return

    context.update({
        'domain': settings.APP_HOST,
        'user': user,
    })

    _send_mail(
        subject_template_name,
        email_template_name_text,
        email_template_name_html,
        context,
        settings.EMAIL_FROM,
        user.email,
        **kwargs,
    )
