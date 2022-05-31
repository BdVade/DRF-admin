from django.db import models


class TestAbstractModel(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        abstract = True


class TestModel(TestAbstractModel):
    age = models.IntegerField
