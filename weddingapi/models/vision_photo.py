from django.db import models


class VisionPhoto(models.Model):
    host = models.ForeignKey(
        "Host", on_delete=models.CASCADE)
    file = models.ImageField(
        upload_to='visionphotos', height_field=None,
        width_field=None, max_length=None)
    time_added = models.DateTimeField(auto_now=True)