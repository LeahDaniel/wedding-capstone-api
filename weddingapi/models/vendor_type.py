from django.db import models


class VendorType(models.Model):
    label = models.CharField(max_length=40)
    image = models.ImageField(
        upload_to='vendortypes', height_field=None,
        width_field=None, max_length=None)
