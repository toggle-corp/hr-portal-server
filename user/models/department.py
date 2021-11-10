from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        null=True,
        help_text='This email is used to send alert to whole department',
    )
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='department-logo/', null=True, blank=True)
    # url = models.URLField(verbose_name=_('URL'), max_length=256)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.name