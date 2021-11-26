import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from .models import Leave
from apps.user.factories import UserFactory


class LeaveFactory(DjangoModelFactory):
    type = fuzzy.FuzzyChoice(Leave.Type)
    status = fuzzy.FuzzyChoice(Leave.Status)
    num_of_days = fuzzy.FuzzyInteger(0, 42)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Leave
