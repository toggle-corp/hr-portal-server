import factory
import datetime
from factory import fuzzy
from factory.django import DjangoModelFactory

from .models import Leave, LeaveDay
from apps.user.factories import UserFactory


class LeaveDayFactory(DjangoModelFactory):
    type = fuzzy.FuzzyChoice(LeaveDay.Type)
    additional_information = fuzzy.FuzzyText(length=50)
    date = fuzzy.FuzzyDate(datetime.date(2022, 1, 1), datetime.date(2023, 1, 1))

    class Meta:
        model = LeaveDay


class LeaveFactory(DjangoModelFactory):
    type = fuzzy.FuzzyChoice(Leave.Type)
    status = fuzzy.FuzzyChoice(Leave.Status)
    num_of_days = fuzzy.FuzzyInteger(0, 42)
    additional_information = fuzzy.FuzzyText(length=50)

    class Meta:
        model = Leave

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        leave = super()._create(model_class, *args, **kwargs)
        LeaveDayFactory.create_batch(5, leave=leave)
        return leave
