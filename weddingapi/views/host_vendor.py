"""View module for handling requests about hostVendors"""
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from weddingapi.models import HostVendor, Host, Vendor
from weddingapi.views.auth import UserSerializer
from .host import HostSerializer


class HostVendorView(ViewSet):
    """HostVendor view"""

    def list(self, request):
        """Handle GET requests to get all hosts

        Returns:
            Response -- JSON serialized list of hosts
        """

        host_vendors = HostVendor.objects.all()
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
            return Response(None)

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
        fields = ("id", "user")


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
        fields = ('vendor',)
