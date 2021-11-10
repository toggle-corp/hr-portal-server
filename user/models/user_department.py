from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User
from .department import Department


class UserDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_department')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='user_department')

    def __str__(self):
        return str(self.name) + " , " + str(self.department)