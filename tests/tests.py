from rest_framework.test import APITestCase, override_settings, APIRequestFactory, URLPatternsTestCase
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.settings import api_settings
from tests.models import TestModel, TestAbstractModel, SecondTestModel
from tests.serializers import AdminSerializer
from tests.permissions import ReadOnly
from tests.pagination import LargeResultsSetPagination
from restadmin.sites import AdminSite, AlreadyRegistered, NotRegistered
from django.core.exceptions import ImproperlyConfigured
from django.urls import path, reverse
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.test.client import RequestFactory


# Create your tests here.


class TestRegistration(APITestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_plain_registration(self):
        self.site.register(TestModel)
        self.assertTrue(issubclass(self.site._registry[TestModel], ModelViewSet))
        viewset = self.site._registry[TestModel]
        self.site.unregister(TestModel)
        registry_viewset_objects = [registry_object[0] for registry_object in self.site.admin_router.registry]
        self.assertFalse(viewset in registry_viewset_objects)
        self.assertEqual(self.site._registry, {})

    def test_unregistering_unregistered_model(self):
        with self.assertRaises(NotRegistered):
            self.site.unregister(TestModel)

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


site = AdminSite()


# @override_settings(ROOT_URLCONF="tests.tests")
class TestViewSets(URLPatternsTestCase):
    databases = '__all__'
    urlpatterns = [
        path("test_admin/", site.urls),
        path("admin-docs/", site.docs)

    ]

    def setUp(self) -> None:
        # self.superuser = User.objects.create_superuser(
        #     username="super", password="secret", email="super@example.com"
        # )
        # self.client.force_login(self.superuser)
        site.register(TestModel)

    def test_docs_generation(self):
        docs_url = reverse("api-docs:docs-index")
        print(docs_url)
        response = self.client.get(docs_url)
        print(response.headers)
        print(response.data)
        self.assertEqual(response.status_code, 200)
