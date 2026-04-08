from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # This tells Django to load your signals.py file 
        # as soon as the 'accounts' app is started.
        import accounts.signals