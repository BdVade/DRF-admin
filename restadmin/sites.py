from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers, viewsets, routers, permissions
from rest_framework.settings import api_settings


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AdminModel:
    pass


class AdminSite:

    def __init__(self):
        self._registry = {}
        self.admin_router = routers.DefaultRouter()

    def register(self, model_or_iterable, serializer: serializers.ModelSerializer = None,
                 permission_class: list = None, pagination_class=None):
        """
        Register Models to the AdminSite. Generates a serializer or uses the one passed.
        """

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    f"The model {model.__name__} is abstract. It cannot be registered with admin")

            if model in self._registry:
                raise AlreadyRegistered(f"The model {model.__name__} has already been registered")
            model_name = model.__name__

            if serializer:
                serializer_class = serializer
            else:
                serializer_class = type(f"{model_name}Serializer", (serializers.ModelSerializer,), {
                    'Meta': type('Meta', (object,), {
                        'model': model,
                        'fields': '__all__'
                    })
                })

            generated_viewset_permission_class = permission_class or [permissions.IsAdminUser]
            generated_viewset_pagination_class = pagination_class or api_settings.DEFAULT_PAGINATION_CLASS

            viewset = type(f"{model_name}ViewSet", (viewsets.ModelViewSet,), {
                'queryset': model.objects.all(),
                'permission_classes': generated_viewset_permission_class,
                'pagination_class': generated_viewset_pagination_class,
                'serializer_class': serializer_class,
            })
            self._registry[model] = viewset
            #
            self.admin_router.register(f"{model._meta.app_label}/{model_name}", viewset, f"admin_{model_name}")

    def get_registry(self):
        return self._registry

    # def get_urls(self):
    #     url_patterns = []
    #     for model, admin_site in self._registry.items():
    #         self.admin_router.register()

    @property
    def urls(self):
        return self.admin_router.urls

    def is_registered(self, model):
        """
        Check If a model is registered
        """
        return model in self._registry


site = AdminSite()