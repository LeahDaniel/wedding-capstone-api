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
            
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all vendors

        Returns:
            Response -- JSON serialized list of vendors
        """

        host = Host.objects.get(user=request.auth.user)

        vendors = Vendor.objects.filter(
            city__iexact=host.city,
            state__iexact=host.state,
            allowed_sizes__wedding_size=host.wedding_size_id
        )

        max_price = request.query_params.get('max_price', None)
        min_price = request.query_params.get('min_price', None)
        rating = request.query_params.get('rating', None)

        if max_price is not None:
            vendors = vendors.annotate(
                cost_average=Avg("contracts__cost_per_hour")
            ).filter(cost_average__lte=max_price)
        if min_price is not None:
            vendors = vendors.annotate(
                cost_average=Avg("contracts__cost_per_hour")
            ).filter(cost_average__gte=min_price)
        if rating is not None:
            vendors = vendors.annotate(
                rating_average=Avg("vendor_rating__score")
            ).filter(rating_average__gte=rating)

        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

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
    vendor_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        depth = 1
        fields = ("id", "user", "vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "profile_image", "years_in_business",
                  "contracts", "average_rating", "average_cost", "total_hired_count",
                  "allowed_sizes", "vendor_reviews")

    def get_vendor_reviews(self, instance):
        """Order the embedded vendor_reviews list"""
        vendor_reviews = instance.vendor_reviews.order_by('-time_sent')
        return ReviewSerializer(vendor_reviews, many=True).data


class UpdateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ("vendor_type", "business_name", "city", "state",
                  "zip_code", "description", "profile_image", "years_in_business")
