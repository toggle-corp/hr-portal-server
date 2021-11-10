from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    primary_email = models.EmailField(unique=True)  # Make email unique
    secondary_email = models.EmailField(unique=True, null=True, blank=True)
    joined_at = models.DateField(null=True, blank=True, help_text='Joined TC')
    avatar_url = models.URLField(null=True, blank=True)
    department = models.ManyToManyField('Department', through='UserDepartment', related_name='user')
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=Gender.choices,
        max_length=10,
        null=True, blank=True,
        help_text='This is used to determine available leave days for an employee.'
    )
    primary_phone_number = models.CharField(verbose_name=_('Phone'), max_length=256,
                             blank=True, null=True)
    secondary_phone_number = models.CharField(verbose_name=_('Secondary Phone'), max_length=256,
                             blank=True, null=True)
    address = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return self.first_name + " " + self.last_name

