from django.db import models


class MyModel(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name
