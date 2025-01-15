from django.apps import AppConfig
from django_q.models import Schedule

class DatabasesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'databases'

    def ready(self):
        """Ensure the Pokémon sync schedule exists."""
        Schedule.objects.get_or_create(
            name="Sync Pokémon Data",
            func="databases.tasks.sync_pokemon",
            schedule_type=Schedule.HOURLY,  # Sync hourly (adjust as needed)
        )
