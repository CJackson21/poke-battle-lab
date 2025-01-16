from django.apps import AppConfig

class DatabasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'databases'

    def ready(self):
        # Import signals or other initialization logic, but avoid accessing models directly
        pass
