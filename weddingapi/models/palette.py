from django.db import models


class Palette(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    color1 = models.CharField(max_length=7)
    color2 = models.CharField(max_length=7)
    color3 = models.CharField(max_length=7)