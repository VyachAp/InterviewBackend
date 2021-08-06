from django.apps import AppConfig


class InterviewConfig(AppConfig):
    name = "interview"

    def ready(self):
        from interview.models.signals import notify
