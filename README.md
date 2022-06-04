# DjangoRestAdmin
A project to generate admin endpoints for models



## Endpoint Documentation

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
## Tests
To run the tests:

From the base directory run :
```
python load_tests.py
```
