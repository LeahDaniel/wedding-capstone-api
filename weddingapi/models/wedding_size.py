from django.db import models


class WeddingSize(models.Model):
    min_guests = models.PositiveSmallIntegerField()
    max_guests = models.PositiveSmallIntegerField(null=True)
    label = models.CharField(max_length=20)
