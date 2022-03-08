from django.db import models


class VendorType(models.Model):
    label = models.CharField(max_length=40)
