from django.apps import AppConfig


class RentalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental'
    
    def ready(self):
        # Import signals to register them
        import rental.signals
    verbose_name = 'Location Simple'
