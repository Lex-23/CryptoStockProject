from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name
