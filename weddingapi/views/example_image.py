import base64
import uuid

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Vendor, ExampleImage


class ExampleImageView(ViewSet):
    """ExampleImage view"""

    def list(self, request):
        """Handle GET requests to get all exampleImages

        Returns:
            Response -- JSON serialized list of exampleImages
        """

        vendor_id = request.query_params.get('vendor', None)

        example_images = ExampleImage.objects.filter(
            vendor__id=vendor_id).order_by("time_added")
        serializer = ExampleImageSerializer(example_images, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized exampleImage instance
        """
        vendor = Vendor.objects.get(user=request.auth.user)
        example_image = ExampleImage()
        try:

            format, imgstr = request.data["file"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                                name=f'{example_image.id}-{uuid.uuid4()}.{ext}')

            example_image.file = data
            example_image.vendor = vendor
            example_image.save()

            serializer = ExampleImageSerializer(example_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """[summary]

        """
        example_image = ExampleImage.objects.get(pk=pk)
        example_image.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ExampleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExampleImage
        fields = ("id", "vendor", "file", "time_added")
