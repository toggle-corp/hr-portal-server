import django_filters

from .models import User


class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'primary_email', 'secondary_email',
            'address', 'primary_phone_number', 'secondary_phone_number', 'joined_at',
            'birthday',
        ]
