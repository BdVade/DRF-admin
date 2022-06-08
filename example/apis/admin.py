from django.contrib import admin
import sys
sys.path.append("..")
import restadmin
from .models import TestModel, SecondTestModel

# Register your models here.

restadmin.site.register(TestModel)
restadmin.site.register(SecondTestModel)
