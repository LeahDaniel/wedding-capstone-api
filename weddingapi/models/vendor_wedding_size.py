from django.db import models


class VendorWeddingSize(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="allowed_sizes")
    wedding_size = models.ForeignKey("WeddingSize", on_delete=models.CASCADE)
