from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    ready_has_run = False 

    def ready(self):
        if not UserConfig.ready_has_run:
            import user.signals
            UserConfig.ready_has_run=True