from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers, viewsets, routers, permissions
from rest_framework.settings import api_settings
from rest_framework.permissions import BasePermission
from rest_framework.documentation import include_docs_urls
from typing import Type, List, Union

from .restmodeladmin import RestModelAdmin


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

    def register(self, model_or_iterable, serializer_or_modeladmin: Union[serializers.ModelSerializer, RestModelAdmin] = None,
                 permission_classes: List[Type[BasePermission]] = None, pagination_class=None):
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
            
            if serializer_or_modeladmin and issubclass(serializer_or_modeladmin, serializers.ModelSerializer):
                serializer_class = serializer_or_modeladmin
            elif serializer_or_modeladmin and issubclass(serializer_or_modeladmin, RestModelAdmin):
                self._register_restmodel_admin(model, serializer_or_modeladmin)
                continue
            else:
                serializer_class = type(f"{model_name}Serializer", (serializers.ModelSerializer,), {
                    'Meta': type('Meta', (object,), {
                        'model': model,
                        'fields': '__all__'
                    })
                })

            generated_viewset_permission_class = permission_classes or [permissions.IsAdminUser]
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
    
    def _register_restmodel_admin(self, model, restmodeladmin):
        """Register RestModelAdmin"""

        self._setup_default_modeladmin(model, restmodeladmin)

        self._registry[model] = restmodeladmin
        #
        self.admin_router.register(f"{model._meta.app_label}/{model.__name__}", restmodeladmin, f"admin_{model.__name__}")

    def _setup_default_modeladmin(self, model, restmodeladmin):
        """Check for required attributes and set defaults if not given"""
        
        # No queryset or get_queryset defined
        if restmodeladmin.queryset is None and not 'get_queryset' in restmodeladmin.__dict__:
            restmodeladmin.queryset = model.objects.all()
        
        # No serializer class or get_serializer_class defined
        if restmodeladmin.serializer_class is None and not 'get_serializer_class' in restmodeladmin.__dict__:
            restmodeladmin.serializer_class = type(f"{model.__name__}Serializer", (serializers.ModelSerializer,), {
                'Meta': type('Meta', (object,), {
                    'model': model,
                    'fields': '__all__'
                })
            })

    def get_registry(self):
        return self._registry

    # def get_urls(self):
    #     url_patterns = []
    #     for model, admin_site in self._registry.items():
    #         self.admin_router.register()

    @property
    def urls(self):
        """

        :return: the router urlconf object, appname, and url namespace
        """
        return self.admin_router.urls, "restadmin", "restadmin"

    def is_registered(self, model):
        """
        Check If a model is registered
        """
        return model in self._registry

    def unregister(self, model):
        """
        Check if the model is in our registry first, Then delete the viewset object from the router registry,
        Then delete from our registry
        """
        model_name = model.__name__
        if model not in self._registry:
            raise NotRegistered(f"The model {model_name} has not been registered")
        viewset = self._registry[model]
        self.admin_router.registry.remove((f"{model._meta.app_label}/{model_name}", viewset, f"admin_{model_name}"))
        del self._registry[model]

    @property
    def docs(self):
        urls = self.urls
        return include_docs_urls(title="RestAdmin Endpoints Documentation", public=True, patterns=urls[0],
                                 permission_classes=[permissions.IsAdminUser])


site = AdminSite()
