from django.apps import AppConfig


class CuentaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cuenta'
    verbose_name = 'Cuenta de Usuario'

    def ready(self):
        import apps.cuenta.signals  # noqa
