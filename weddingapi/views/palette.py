from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Palette, Host


class PaletteView(ViewSet):
    """Palette view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single palette

        Returns:
            Response -- JSON serialized palette
        """
        try:
            host = Host.objects.get(pk=pk)
            palette = Palette.objects.get(host=host)

            serializer = PaletteSerializer(palette)
            return Response(serializer.data)
        except Palette.DoesNotExist:
            return Response({'found': False})

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized palette instance
        """
        host = Host.objects.get(user=request.auth.user)
        try:
            serializer = CreatePaletteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(host=host)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'palette': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a palette

        Returns:
            Response -- Empty score with 204 status code
        """
        try:
            palette = Palette.objects.get(pk=pk)
            serializer = CreatePaletteSerializer(palette, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'palette': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path="current")
    def get_current(self, request):
        """Handle GET requests for single palette

        Returns:
            Response -- JSON serialized palette
        """
        try:
            host = Host.objects.get(user=request.auth.user)
            palette = Palette.objects.get(host=host)

            serializer = PaletteSerializer(palette)
            return Response(serializer.data)
        except Palette.DoesNotExist:
            return Response({'found': False})


class PaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palette
        fields = ("id", "host", "color1", "color2", "color3")


class CreatePaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palette
        fields = ("id", "color1", "color2", "color3")
