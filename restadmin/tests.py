from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet
from restadmin.models import TestModel, TestAbstractModel
from restadmin.sites import AdminSite, AlreadyRegistered
from django.core.exceptions import ImproperlyConfigured


# Create your tests here.


class TestRegistration(APITestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_plain_registration(self):
        self.site.register(TestModel)
        self.assertTrue(issubclass(self.site._registry[TestModel], ModelViewSet))

        # self.site.unregister(TestModel)
        # self.assertEqual(self.site._registry, {})

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
