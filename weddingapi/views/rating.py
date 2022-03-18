from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Rating, Host
from weddingapi.models.vendor import Vendor


class RatingView(ViewSet):
    """Rating view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating
        """
        try:
            host = Host.objects.get(user=request.auth.user)
            vendor = Vendor.objects.get(pk=pk)
            
            rating = Rating.objects.get(host=host,vendor=vendor)

            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist:
            return Response({'found': False})

    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """

        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rating instance
        """
        host = Host.objects.get(user=request.auth.user)
        try:
            serializer = CreateRatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(host=host)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'rating': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a rating

        Returns:
            Response -- Empty score with 204 status code
        """
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = CreateRatingSerializer(rating, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'rating': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        """[summary]

        Args:
            request ([type]): [description]
            pk ([type]): [description]

        Returns:
            [type]: [description]
        """
        rating = Rating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "vendor", "host", "score")


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("vendor", "score")
