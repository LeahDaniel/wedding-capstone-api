from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
