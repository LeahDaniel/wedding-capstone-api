from django.contrib.auth.models import User
from django.db import models
from datetime import date

from weddingapi.models.host_vendor import HostVendor


class Host(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="host_user")
    wedding_size = models.ForeignKey(
        "WeddingSize", on_delete=models.SET_NULL, null=True)
    profile_image = models.ImageField(
        upload_to='hostprofile', height_field=None,
        width_field=None, max_length=None, null=True)
    date = models.DateField()
    time = models.TimeField()
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=85)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    @property
    def has_happened(self):
        """ Boolean for whether the wedding has already occurred """
        today = date.today()

        if self.date <= today:
            return True
        else:
            return False
        
    @property
    def total_costs(self):
        """ sum of all costs per hour for associated hostVendors """
        
        total_cost = 0
        
        host_vendors =  HostVendor.objects.filter(
                host=self,
                hired=True,
                fired=False
            )
        
        for host_vendor in host_vendors:
            total_cost += host_vendor.cost_per_hour
            
        return total_cost
        
