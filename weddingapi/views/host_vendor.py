"""View module for handling requests about hostVendors"""
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from weddingapi.models import HostVendor, Host
from weddingapi.models.vendor import Vendor
from weddingapi.views.auth import UserSerializer
from .host import HostSerializer
from datetime import date


class HostVendorView(ViewSet):
    """HostVendor view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single hostVendor

        Returns:
            Response -- JSON serialized hostVendor
        """
        try:
            host_vendor = HostVendor.objects.get(pk=pk)

            serializer = HostVendorSerializer(host_vendor)
            return Response(serializer.data)
        except HostVendor.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all host vendors

        Returns:
            Response -- JSON serialized list of host vendors
        """
        today = date.today()
        user = request.auth.user
        if user.is_staff is False:
            host = Host.objects.get(user=user)
            host_vendors = HostVendor.objects.filter(
                host=host,
                hired=True,
                fired=False
            )
        else:
            vendor = Vendor.objects.get(user=user)
            host_vendors = HostVendor.objects.filter(
                vendor=vendor,
                hired=True,
                fired=False,
                host__date__gte=today
            )

        serializer = HostVendorSerializer(host_vendors, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized hostVendor instance
        """
        host = Host.objects.get(user=request.auth.user)

        try:
            serializer = CreateHostVendorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(host=host)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """[summary]

        """
        host_vendor = HostVendor.objects.get(pk=pk)
        host_vendor.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path="contract")
    def find_contract(self, request):
        """Add a cost per hour to a hostVendor relationship"""

        try:
            vendor_id = request.query_params.get('vendor', None)
            host_id = request.query_params.get('host', None)

            if vendor_id and host_id:
                host_vendor = HostVendor.objects.get(
                    vendor_id=vendor_id, host_id=host_id)

            serializer = HostVendorSerializer(host_vendor, many=False)
            return Response(serializer.data)
        except HostVendor.DoesNotExist:
            return Response({"found": False})

    @action(methods=['put'], detail=True, url_path="quote")
    def add_quote(self, request, pk):
        """Add a cost per hour to a hostVendor relationship"""

        host_vendor = HostVendor.objects.get(pk=pk)

        host_vendor.cost_per_hour = request.data["cost_per_hour"]
        host_vendor.save()

        serializer = HostVendorSerializer(host_vendor, many=False)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path="hire")
    def hire(self, request, pk):
        """Add a cost per hour to a hostVendor relationship"""

        host_vendor = HostVendor.objects.get(pk=pk)
        host_vendor.hired = True
        host_vendor.save()

        serializer = HostVendorSerializer(host_vendor, many=False)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path="fire")
    def fire(self, request, pk):
        """Add a cost per hour to a hostVendor relationship"""

        host_vendor = HostVendor.objects.get(pk=pk)

        host_vendor.fired = True
        host_vendor.save()

        serializer = HostVendorSerializer(host_vendor, many=False)
        return Response(serializer.data)


class SimpleVendorSerializer(serializers.ModelSerializer):
    """JSON serializer for vendor types
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Vendor
        depth = 1
        fields = ("id", "user", "vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "profile_image", "years_in_business",
                  "average_rating", "average_cost", "total_hired_count")


class HostVendorSerializer(serializers.ModelSerializer):
    """JSON serializer for hostVendors
    """
    host = HostSerializer(many=False)
    vendor = SimpleVendorSerializer(many=False)

    class Meta:
        model = HostVendor
        depth = 2
        fields = ('id', 'vendor', 'host', 'cost_per_hour', 'hired', 'fired')


class CreateHostVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostVendor
        fields = ('id', 'vendor')
