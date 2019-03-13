from django.apps import AppConfig


class PublicationConfig(AppConfig):
    name = 'publication'

    def ready(self):
        import publication.signals
