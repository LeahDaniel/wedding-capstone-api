from django.contrib.auth.models import User
from django.db import models


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor_type = models.ForeignKey("VendorType", on_delete=models.DO_NOTHING)
    business_name = models.CharField(max_length=85)
    profile_image = models.ImageField(
        upload_to='vendorprofile', height_field=None,
        width_field=None, max_length=None, null=True)
    city = models.CharField(max_length=85)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    description = models.TextField()
    years_in_business = models.PositiveSmallIntegerField()
