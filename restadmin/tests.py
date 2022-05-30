from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet
from .models import TestModel, TestAbstractModel
from .sites import AdminSite


# Create your tests here.


class TestResgistration(APITestCase):
    def setup(self):
        self.site = AdminSite()

    def test_plain_registration(self):
        self.site.register(TestModel)
        self.assertIsInstance(self.site._registry[TestModel], ModelViewSet)

        # self.site.unregister(TestModel)
        # self.assertEqual(self.site._registry, {})

