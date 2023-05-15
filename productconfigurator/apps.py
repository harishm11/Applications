from django.apps import AppConfig
from django.db import models


class ProductconfiguratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productconfigurator'

    def createModel(self, name, fields=None, options=None, bases=None, **kwargs):
        """
        Create a Django model dynamically.
        """
        # Use Django's model factory to create the new model class
        return type(name, bases or (models.Model,), fields or {}, **kwargs)
