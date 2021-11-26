from django.apps import AppConfig


class LeaveConfig(AppConfig):
    name = 'apps.leave'

    def ready(self):
        import apps.leave.signals
