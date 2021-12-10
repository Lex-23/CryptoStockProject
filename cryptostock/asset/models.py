from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name
