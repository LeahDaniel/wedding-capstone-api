from django.db import models


class ExampleImage(models.Model):
    vendor = models.ForeignKey(
        "Vendor", on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='exampleimages', height_field=None,
        width_field=None, max_length=None)
    time_added = models.DateTimeField(auto_now=True)