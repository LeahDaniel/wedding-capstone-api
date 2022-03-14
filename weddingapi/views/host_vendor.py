"""View module for handling requests about hostVendors"""
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from weddingapi.models import HostVendor, Host
from weddingapi.models.vendor import Vendor


class HostVendorView(ViewSet):
    """HostVendor view"""

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

    @action(methods=['put'], detail=False, url_path="quote")
    def add_quote(self, request):
        """Add a cost per hour to a hostVendor relationship"""

        vendor = Vendor.objects.get(user=request.auth.user)

        host_vendor = HostVendor.objects.get(
            host_id=request.data["host_id"],
            vendor=vendor
        )

        host_vendor.cost_per_hour = request.data["cost_per_hour"]

        serializer = HostVendorSerializer(host_vendor, many=False)
        return Response(serializer.data)

    @action(methods=['put'], detail=False, url_path="hire")
    def hire(self, request):
        """Add a cost per hour to a hostVendor relationship"""

        host = Host.objects.get(user=request.auth.user)

        host_vendor = HostVendor.objects.get(
            vendor_id=request.data["vendor_id"],
            host=host
        )

        host_vendor.hired = True

        serializer = HostVendorSerializer(host_vendor, many=False)
        return Response(serializer.data)
    
    @action(methods=['put'], detail=False, url_path="fire")
    def fire(self, request):
        """Add a cost per hour to a hostVendor relationship"""

        host = Host.objects.get(user=request.auth.user)

        host_vendor = HostVendor.objects.get(
            vendor_id=request.data["vendor_id"],
            host=host
        )

        host_vendor.fired = True

        serializer = HostVendorSerializer(host_vendor, many=False)
        return Response(serializer.data)


class HostVendorSerializer(serializers.ModelSerializer):
    """JSON serializer for hostVendors
    """

    class Meta:
        model = HostVendor
        depth = 1
        fields = ('id', 'vendor', 'host', 'cost_per_hour', 'hired', 'fired')


class CreateHostVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostVendor
        fields = ('vendor',)

