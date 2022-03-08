from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
