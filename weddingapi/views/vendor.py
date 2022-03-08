"""View module for handling requests about vendors"""
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from weddingapi.models import Vendor
from .auth import UserSerializer


class VendorView(ViewSet):
    """Vendor view"""

    @action(methods=['get'], detail=False, url_path="profile")
    def get_current(self, request):
        """Get the currently logged in vendor back"""
        try:
            vendor = Vendor.objects.get(user=request.auth.user)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({
                'message': 'The logged in user is not a vendor'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=['put'], detail=False, url_path="updatebusiness")
    def update_current(self, request):
        """put request to currently logged in vendor"""
        try:
            vendor = Vendor.objects.get(user=request.auth.user)
            serializer = UpdateVendorSerializer(vendor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({
                'message': 'The logged in user is not a vendor'},
                status=status.HTTP_404_NOT_FOUND
            )


class VendorSerializer(serializers.ModelSerializer):
    """JSON serializer for vendor types
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Vendor
        depth = 1
        fields = "__all__"


class UpdateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "profile_image", "years_in_business")
