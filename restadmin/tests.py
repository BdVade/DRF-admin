from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.settings import api_settings
from restadmin.models import TestModel, TestAbstractModel, SecondTestModel
from restadmin.serializers import AdminSerializer
from restadmin.permissions import ReadOnly
from restadmin.pagination import LargeResultsSetPagination
from restadmin.sites import AdminSite, AlreadyRegistered
from django.core.exceptions import ImproperlyConfigured


# Create your tests here.


class TestRegistration(APITestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_plain_registration(self):
        self.site.register(TestModel)
        self.assertTrue(issubclass(self.site._registry[TestModel], ModelViewSet))
        self.site.unregister(TestModel)
        # check if unregistered from router
        registry_viewset_objects = [registry_object[0]for registry_object in self.site.admin_router.registry]
        self.assertFalse(self.site._registry[TestModel] in registry_viewset_objects)
        self.assertEqual(self.site._registry, {})

    def test_prevent_double_registration(self):
        self.site.register(TestModel)
        with self.assertRaises(AlreadyRegistered):
            self.site.register(TestModel)

    def test_get_registry(self):
        self.site.register(TestModel)
        self.assertEqual(self.site._registry, self.site.get_registry())

    def test_abstract_model_registration(self):
        with self.assertRaises(ImproperlyConfigured):
            self.site.register(TestAbstractModel)

    def test_is_registered_registered_model(self):
        self.site.register(TestModel)
        self.assertTrue(self.site.is_registered(TestModel))

    def test_is_registered_unregistered_model(self):
        self.assertFalse(self.site.is_registered(TestModel))

    def test_iterable_registration(self):
        self.site.register([TestModel, SecondTestModel])
        self.assertTrue(issubclass(self.site._registry[TestModel], ModelViewSet))
        self.assertTrue(issubclass(self.site._registry[SecondTestModel], ModelViewSet))

    def test_custom_serializer_registration(self):
        self.site.register(TestModel, serializer=AdminSerializer)
        self.assertEqual(self.site._registry[TestModel].serializer_class, AdminSerializer)

    def test_custom_permission_class_registration(self):
        self.site.register(TestModel, permission_classes=[ReadOnly])
        self.assertEqual(self.site._registry[TestModel].permission_classes, [ReadOnly])

    def test_custom_pagination_class_registration(self):
        self.site.register(TestModel, pagination_class=LargeResultsSetPagination)
        self.assertEqual(self.site._registry[TestModel].pagination_class, LargeResultsSetPagination)

    def test_default_serializer_registration(self):
        self.site.register(TestModel)
        self.assertEqual(self.site._registry[TestModel].serializer_class.__name__, 'TestModelSerializer')

    def test_default_permission_class_registration(self):
        self.site.register(TestModel, )
        self.assertEqual(self.site._registry[TestModel].permission_classes, [IsAdminUser])

    def test_default_pagination_class_registration(self):
        self.site.register(TestModel)
        self.assertEqual(self.site._registry[TestModel].pagination_class, api_settings.DEFAULT_PAGINATION_CLASS)
