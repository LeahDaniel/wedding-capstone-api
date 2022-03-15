from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from weddingapi.models import WeddingSize, VendorType


class WeddingSizeSerializer(serializers.ModelSerializer):
    """JSON serializer for weddingSizes
    """
    class Meta:
        model = WeddingSize
        fields = ['id', 'min_guests', 'max_guests', 'label']


class VendorTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for vendorTypes
    """
    class Meta:
        model = VendorType
        fields = ['id', 'label']


@api_view(['GET'])
@permission_classes([AllowAny])
def get_wedding_sizes(request):
    """Handle GET requests to get all weddingSizes

    Returns:
        Response -- JSON serialized list of weddingSizes
    """

    wedding_sizes = WeddingSize.objects.all()
    serializer = WeddingSizeSerializer(wedding_sizes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_vendor_types(request):
    """Handle GET requests to get all vendorTypes

    Returns:
        Response -- JSON serialized list of vendorTypes
    """

    vendor_types = VendorType.objects.all()
    serializer = VendorTypeSerializer(vendor_types, many=True)
    return Response(serializer.data)
