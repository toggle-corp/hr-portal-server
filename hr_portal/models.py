from django.db import models

from hr_portal.middlewares import get_current_user
from apps.user.models import User


class UserResourceModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name='%(class)s_created',
        default=None, blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        User,
        related_name='%(class)s_modified',
        default=None, blank=True, null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        def _set_user_info(instance):
            current_user = get_current_user()
            if current_user is None or current_user.is_anonymous:
                return instance
            self.modified_by = current_user
            if instance.pk is None:
                self.created_by = current_user
            return instance

        _set_user_info(self)
        return super().save(*args, **kwargs)
