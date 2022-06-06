# DjangoRestAdmin
A project to generate admin endpoints for models

## Requirements
- [Django](https://docs.djangoproject.com/en/4.0/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

## Installation


## Usage
- Import restadmin in the admin.py 
- Call `restadmin.site.register(Model)` Model being the model to register 
- Add rest admin to your urls.py file 


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

Using this would require you to have your default schema Class set in your REST_FRAMWORK config in your settings.py file
E.g

```
REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }
```
Run your server and you can find the documentation at ` http://127.0.0.1:8000/restadmin-docs`
## Tests
To run the tests:

From the base directory run :
```
python load_tests.py
```
