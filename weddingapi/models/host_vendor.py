from django.db import models


class HostVendor(models.Model):
    vendor = models.ForeignKey(
        "Vendor", on_delete=models.CASCADE, related_name="contracts")
    host = models.ForeignKey(
        "Host", on_delete=models.CASCADE, related_name="vendors_in_process_with")
    cost_per_hour = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, default=None)
    hired = models.BooleanField(default=False)
    fired = models.BooleanField(default=False)
