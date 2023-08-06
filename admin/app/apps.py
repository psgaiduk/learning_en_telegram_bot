from contextlib import suppress
from importlib import import_module

from django.apps import AppConfig


class CustomAppConfig(AppConfig):

    def ready(self) -> None:

        with suppress(ModuleNotFoundError):
            import_module(f'{self.name}.receivers')


class MainConfig(CustomAppConfig):
    name = 'apps.main'
    verbose_name = 'Основные данные'
