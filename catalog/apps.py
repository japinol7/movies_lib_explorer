from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        from catalog.config.config import update_config_settings
        from tools.logger.logger import log
        try:
            from catalog.models.settings import Settings
            log.info("Load or create default settings object")
            update_config_settings(Settings)
        except Exception as e:
            log.warning("Cannot load or create default settings object. Error: %s", e)
