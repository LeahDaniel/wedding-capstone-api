"""View module for handling requests about hosts"""
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from weddingapi.models import Host
from .auth import UserSerializer


class HostView(ViewSet):
    """Host view"""

    @action(methods=['get'], detail=False, url_path="profile")
    def get_current(self, request):
        """Get the currently logged in host back"""
        try:
            host = Host.objects.get(user=request.auth.user)
            serializer = HostSerializer(host)
            return Response(serializer.data)
        except Host.DoesNotExist:
            return Response({
                'message': 'The logged in user is not a host'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=['put'], detail=False, url_path="updatewedding")
    def update_current(self, request):
        """put request to currently logged in host"""
        try:
            host = Host.objects.get(user=request.auth.user)
            serializer = UpdateHostSerializer(host, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Host.DoesNotExist:
            return Response({
                'message': 'The logged in user is not a host'},
                status=status.HTTP_404_NOT_FOUND
            )



class HostSerializer(serializers.ModelSerializer):
    """JSON serializer for host types
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Host
        depth = 1
        fields = "__all__"


class UpdateHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ("wedding_size", "date", "time",
                  "street_address", "city", "state", "zip_code")
