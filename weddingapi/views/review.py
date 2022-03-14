from rest_framework import serializers
from weddingapi.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("vendor", "host", "body", "time_sent")