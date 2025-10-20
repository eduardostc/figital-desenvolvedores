from django.apps import AppConfig

class FigitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'figital'

    def ready(self):
        from . import signals  # Importa os sinais para serem ativados
