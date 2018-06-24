from django.apps import AppConfig


class StockConfig(AppConfig):
    name = 'stock'

    def ready(self):
        # Making sure that all signals are active when the app is loaded
        from stock import signals # NOQA
