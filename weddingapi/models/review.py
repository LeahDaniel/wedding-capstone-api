from django.db import models


class Review(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="vendor_review")
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    body = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)
