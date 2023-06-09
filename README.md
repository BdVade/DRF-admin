# DRF-Admin
A package to generate CRUD endpoints for registered models with the Django-REST Framework. 

## Requirements
- [Django](https://docs.djangoproject.com/en/4.0/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

## Installation
To install run:

`pip install drf-admin`

## Usage
- Import restadmin in the admin.py 
- Call `restadmin.site.register(Model)` Model being the model to register 
- Add rest admin to your urls.py file 

## Prerequisite
- rest_framework should be properly set up to use this package hitch free

A sample of it's configuration in the settings file:
```python
 REST_FRAMEWORK={
            'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
            'TEST_REQUEST_RENDERER_CLASSES': [
                'rest_framework.renderers.MultiPartRenderer',
                'rest_framework.renderers.JSONRenderer',
                'rest_framework.renderers.TemplateHTMLRenderer', ],
            "DEFAULT_AUTHENTICATION_CLASSES": [
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.BasicAuthentication'
            ],
            "DEFAULT_PERMISSION_CLASSES": [
                'rest_framework.permissions.AllowAny',
            ]
        }
```

For example: 

models.py
```python
from django.db import models

class TestModel(models.Model):
    age = models.IntegerField()
```

admin.py
```python
from .models import TestModel
import restadmin

restadmin.site.register(TestModel)
```
urls.py
```python
from restadmin import site
from django.urls import path




urlpatterns = [
    ...
    path('restadmin/', site.urls),
    ...
]
```

## Customization
This package allows you to specify the following when registering your model
- `serializer_or_modeladmin`: A Model Serializer Class or a subclass of `RestModelAdmin`
- ` permission_classes`: A list of Permission classes
- `pagination_classs`: A Pagination Class

An example of how a call to the register method with all 3 would look is :
```python
restadmin.site.register(TestModel, serializer_or_modeladmin=AdminSerializer, permission_classes=[ReadOnly], 
                        pagination_class=LargeResultsSetPagination)

```

`RestModelAdmin` expose the same interface as `ModelViewSet` so you can add the whole customizations that
`ModelViewSet` offers. This includes:

- Custom querysets
- redifining defaults methods
- add actions as ModelViewSet's exta actions

You can also register models with the `register` decorator

Example:
```python
from restadmin import register, RestModelAdmin
from .models import TestModel

@register(TestModel)
class TestRestModelAdmin(RestModelAdmin):

    serializer_class = MyCustomSerializer # Optional. A default is provided if None defined

    def get_queryset(self):
        queryset = TestModel.objects.filter(age__lt=30)
        return queryset

```

## Endpoint Documentation
* This requires you to have coreapi installed

A page to document the Endpoints generated can be accessed by adding the following to your base urls file

```python
from restadmin import site


urlpatterns = [
   ...
    path('restadmin-docs/', site.docs)
    ...
]
```


Using this would require you to have your default schema Class set in your REST_FRAMEWORK config in your settings.py file
E.g

```
REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }
```
Run your server and you can find the documentation at ` http://127.0.0.1:8000/restadmin-docs`
NOTE: The Documentation page is restricted to staff only(is_staff has to be True)
## Tests
To run the tests:

From the base directory run :
```
python load_tests.py
```
