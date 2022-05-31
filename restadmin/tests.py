from rest_framework.test import APITestCase
from rest_framework.viewsets import ModelViewSet
from restadmin.models import TestModel
from restadmin.sites import AdminSite


# Create your tests here.


class TestRegistration(APITestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_plain_registration(self):
        self.site.register(TestModel)
        self.assertTrue(issubclass(self.site._registry[TestModel], ModelViewSet))

        # self.site.unregister(TestModel)
        # self.assertEqual(self.site._registry, {})

