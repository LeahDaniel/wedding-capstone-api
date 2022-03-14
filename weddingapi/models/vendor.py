from django.contrib.auth.models import User
from django.db import models
from .host_vendor import HostVendor
from .rating import Rating


class Vendor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="vendor_user")
    vendor_type = models.ForeignKey(
        "VendorType", on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=85)
    profile_image = models.ImageField(
        upload_to='vendorprofile', height_field=None,
        width_field=None, max_length=None, null=True)
    city = models.CharField(max_length=85)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    description = models.TextField()
    years_in_business = models.PositiveSmallIntegerField()
    wedding_sizes = models.ManyToManyField(
        "WeddingSize", through="VendorWeddingSize", related_name="vendor_wedding_sizes")

    @property
    def average_rating(self):
        """ Average of rating scores """
        ratings = Rating.objects.filter(vendor=self)

        total_rating = 0

        if len(ratings) > 0:
            for rating in ratings:
                total_rating += rating.score

            return total_rating / len(ratings)
        else:
            return None

    @property
    def average_cost(self):
        """ Average of hourly costs """

        host_vendors = HostVendor.objects.filter(vendor=self)

        total_cost = 0

        if len(host_vendors) > 0:
            for contract in host_vendors:
                total_cost += contract.cost_per_hour

            return total_cost / len(host_vendors)
        else:
            return None

    @property
    def total_hired_count(self):
        """ Average of hourly costs """

        host_vendors = HostVendor.objects.filter(vendor=self)

        return len(host_vendors)
