from core.models import DatabaseConfig


def get_database_config(self):
    database_conf = DatabaseConfig.objects.get(pk=1)
    return database_conf
