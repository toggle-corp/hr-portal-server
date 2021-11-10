# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class Department(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(
#         null=True,
#         help_text='This email is used to send alert to whole department',
#     )
#     description = models.TextField(blank=True)
#     logo = models.ImageField(upload_to='department-logo/', null=True, blank=True)
#     # url = models.URLField(verbose_name=_('URL'), max_length=256)

#     class Meta:
#         verbose_name = _('User Department')
#         verbose_name_plural = _('User Departments')

#     def __str__(self):
#         return self.name


# class User(AbstractUser):
#     class Gender(models.TextChoices):
#         MALE = 'male', 'Male'
#         FEMALE = 'female', 'Female'

#     primary_email = models.EmailField(unique=True)  # Make email unique
#     secondary_email = models.EmailField(unique=True, null=True, blank=True)
#     joined_at = models.DateField(null=True, blank=True, help_text='Joined TC')
#     avatar_url = models.URLField(null=True, blank=True)
#     department = models.ManyToManyField('Department', through='UserDepartment', related_name='user_department')
#     birthday = models.DateField(null=True, blank=True)
#     gender = models.CharField(
#         choices=Gender.choices,
#         max_length=10,
#         null=True, blank=True,
#         help_text='This is used to determine available leave days for an employee.'
#     )
#     primary_phone_number = models.CharField(verbose_name=_('Phone'), max_length=256,
#                              blank=True, null=True)
#     secondary_phone_number = models.CharField(verbose_name=_('Secondary Phone'), max_length=256,
#                              blank=True, null=True)
#     address = models.CharField(max_length=500, null=True, blank=True)


# class UserDepartment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
