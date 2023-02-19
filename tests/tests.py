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
import pdb


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
        self.site.register(TestModel, serializer_or_modeladmin=AdminSerializer)
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
site.register(TestModel)

urlpatterns = [
    path("test_admin/", site.urls),
    path("admin-docs/", site.docs)

]


@override_settings(ROOT_URLCONF="tests.tests")
class TestViewSets(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="super", password="secret", email="super@example.com"
        )
        self.client.force_login(self.superuser)

    def test_docs_generation(self):
        docs_url = reverse("api-docs:docs-index")
        response = self.client.get(docs_url)
        self.assertIn("TestModel", response.data)
        self.assertEqual(response.status_code, 200)

    def test_list_model_objects(self):
        url = reverse("restadmin:admin_TestModel-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_model_endpoint(self):
        url = reverse("restadmin:admin_TestModel-list")
        response = self.client.post(url, data={"name": "name", "age": 16})
        self.assertEqual(TestModel.objects.count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_update_model_endpoint(self):
        model_object = TestModel.objects.create(name="name1", age=5)
        url = reverse("restadmin:admin_TestModel-detail", args=(model_object.id,))
        response = self.client.put(url, data={"name": "name2", "age": 15})
        new_object = TestModel.objects.get(id=model_object.id)
        self.assertEqual(new_object.age, 15)
        self.assertEqual(new_object.name, "name2")

    def test_partial_update_model_endpoint(self):
        model_object = TestModel.objects.create(name="name1", age=5)
        url = reverse("restadmin:admin_TestModel-detail", args=(model_object.id,))
        response = self.client.patch(url, data={"age": 15})
        new_object = TestModel.objects.get(id=model_object.id)
        self.assertEqual(new_object.age, 15)


    def test_get_model_endpoint(self):
        model_object = TestModel.objects.create(name="name1", age=5)
        url = reverse("restadmin:admin_TestModel-detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_delete_model_endpoint(self):
        model_object = TestModel.objects.create(name="name1", age=5)
        self.assertEqual(TestModel.objects.count(), 1)
        url = reverse("restadmin:admin_TestModel-detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(TestModel.objects.count(), 0)
