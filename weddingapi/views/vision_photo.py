import base64
import uuid

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Host, VisionPhoto
from weddingapi.views.host import HostSerializer


class VisionPhotoView(ViewSet):
    """VisionPhoto view"""

    def list(self, request):
        """Handle GET requests to get all visionPhotos

        Returns:
            Response -- JSON serialized list of visionPhotos
        """
        
        host_id = request.query_params.get('host', None)

        vision_photos = VisionPhoto.objects.filter(host__id=host_id)
        serializer = VisionPhotoSerializer(vision_photos, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized visionPhoto instance
        """
        host = Host.objects.get(user=request.auth.user)
        vision_photo = VisionPhoto()
        try:

            format, imgstr = request.data["file"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                                name=f'{vision_photo.id}-{uuid.uuid4()}.{ext}')

            vision_photo.file = data
            vision_photo.host = host
            vision_photo.save()
            
            serializer = VisionPhotoSerializer(vision_photo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """[summary]

        """
        visionPhoto = VisionPhoto.objects.get(pk=pk)
        visionPhoto.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class VisionPhotoSerializer(serializers.ModelSerializer):
    host = HostSerializer(many=False)

    class Meta:
        model = VisionPhoto
        fields = ("id", "host", "file", "time_added")
