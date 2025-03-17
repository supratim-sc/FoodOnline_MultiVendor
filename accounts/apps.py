from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    '''
        Signal handlers are usually defined in a signals submodule of the application they relate to. Signal receivers are connected in the ready() method of your application configuration class (app.py). If you’re using the receiver() decorator, import the signals submodule inside ready(), this will implicitly connect signal handlers:    
    '''
    # Registering the signal in the app so that when the app loads or gets ready, the signals will also load instantly
    def ready(self):
        import accounts.signals