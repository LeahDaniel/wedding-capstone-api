"""View module for handling requests about vendors"""
from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Host, Vendor
from weddingapi.views.review import ReviewSerializer

from .auth import UserSerializer


class VendorView(ViewSet):
    """Vendor view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single vendor

        Returns:
            Response -- JSON serialized vendor
        """
        try:
            vendor = Vendor.objects.get(pk=pk)

            serializer = SingleVendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all vendors

        Returns:
            Response -- JSON serialized list of vendors
        """

        host = Host.objects.get(user=request.auth.user)
        type_id = request.query_params.get('type', None)
        rating = request.query_params.get('rating', None)

        vendors = Vendor.objects.filter(
            city__iexact=host.city,
            state__iexact=host.state,
            allowed_sizes__wedding_size=host.wedding_size_id,

        )

        if type_id is not None:
            vendors = vendors.filter(vendor_type_id=type_id)
        if rating is not None:
            vendors = vendors.annotate(
                rating_average=Avg("vendor_rating__score")
            ).filter(rating_average__gte=rating)

        serializer = SimpleVendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path="profile")
    def get_current(self, request):
        """Get the currently logged in vendor back"""
        try:
            vendor = Vendor.objects.get(user=request.auth.user)
            serializer = SingleVendorSerializer(vendor)
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


class SimpleVendorSerializer(serializers.ModelSerializer):
    """JSON serializer for vendor types
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Vendor
        depth = 2
        fields = ("id", "user", "vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "profile_image", "years_in_business",
                  "average_rating", "average_cost", "total_hired_count")


class SingleVendorSerializer(serializers.ModelSerializer):
    """JSON serializer for vendor types
    """
    user = UserSerializer(many=False)
    vendor_reviews = serializers.SerializerMethodField()
    # contracts = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        depth = 1
        fields = ("id", "user", "vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "profile_image", "years_in_business",
                  "average_rating", "average_cost", "total_hired_count",
                  "allowed_sizes", "vendor_reviews")

    def get_vendor_reviews(self, instance):
        """Order the embedded vendor_reviews list"""
        vendor_reviews = instance.vendor_reviews.order_by('-time_sent')
        return ReviewSerializer(vendor_reviews, many=True).data

    # def get_contracts(self, instance):
    #     """Filter the embedded contracts list"""
        
    #     contracts = instance.contracts.filter(hired=True, fired=False)
    #     return HostVendorSerializer(contracts, many=True).data


class UpdateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "years_in_business", "allowed_sizes")
