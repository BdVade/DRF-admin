from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AdminModel:
    pass


class AdminSite:

    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, admin_class):
        # TODO: Add a default admin class
        # TODO: Already registered Error
        """
        Register Models to the AdminSite. Uses the AdminClass passed to direct what is generated
        """

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    f"The model {model.__name__} is abstract. It cannot be registered with admin")
            self._registry[model] = admin_class(model, self)

    def get_registry(self):
        return self._registry

    def get_urls(self):
        pass

    def is_registered(self, model):
        """
        Check If a model is registered
        """
        return model in self._registry

    def has_permission(self):
        pass