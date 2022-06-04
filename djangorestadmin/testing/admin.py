from django.contrib import admin
import sys
sys.path.append("..")
import restadmin
from .models import TestModel

# Register your models here.

restadmin.site.register(TestModel)
