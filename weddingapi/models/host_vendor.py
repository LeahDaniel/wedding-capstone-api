from django.db import models


class HostVendor(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    cost_per_hour = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, default=None)
    hired = models.BooleanField(default=False)
    fired = models.BooleanField(default=False)
