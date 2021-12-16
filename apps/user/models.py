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
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)
    department = models.ManyToManyField('Department', through='UserDepartment', related_name='user')
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=Gender.choices,
        max_length=10,
        default=Gender.MALE,
        null=True, blank=True,
        help_text='Choose Gender'
    )
    primary_phone_number = models.CharField(verbose_name=_('Phone'), max_length=256, blank=True, null=True)
    secondary_phone_number = models.CharField(verbose_name=_('Secondary Phone'), max_length=256, blank=True, null=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

    @property
    def total_leaves_days(self):
        if self.gender == User.Gender.FEMALE:
            return 24  # 4+ Maternity Leave
        return 20

    @property
    def full_name(self):
        return self.get_full_name()


class Department(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        null=True,
        help_text='This email is used to send alert to whole department',
    )
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='department-logo/', null=True, blank=True)
    logo_url = models.URLField(verbose_name=_('Logo URL'), null=True, blank=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.name


class UserDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_department')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='user_department')

    def __str__(self):
        return str(self.user) + " , " + str(self.department)
