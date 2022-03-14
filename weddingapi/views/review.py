from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Review, Host


class ReviewView(ViewSet):
    """Review view"""
    
    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of reviews
        """

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized review instance
        """
        host = Host.objects.get(user=request.auth.user)
        try:
            serializer = CreateReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(host=host)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'review': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = CreateReviewSerializer(review, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'review': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """[summary]

        """
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "vendor", "host", "body", "time_sent")


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("vendor", "body")
