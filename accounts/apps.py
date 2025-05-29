from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Импорт после полной загрузки приложений
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from . import signals