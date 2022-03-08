from django.contrib.auth.models import User
from django.db import models


class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wedding_size = models.ForeignKey(
        "WeddingSize", on_delete=models.DO_NOTHING)
    profile_image = models.ImageField(
        upload_to='hostprofile', height_field=None,
        width_field=None, max_length=None, null=True)
    date = models.DateField()
    time = models.TimeField()
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=85)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
