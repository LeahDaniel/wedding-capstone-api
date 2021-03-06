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
    
    def retrieve(self, request, pk):
        """Handle GET requests for single host

        Returns:
            Response -- JSON serialized host
        """
        try:
            host = Host.objects.get(pk=pk)
            serializer = HostSerializer(host)
            return Response(serializer.data)
        except Host.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all hosts

        Returns:
            Response -- JSON serialized list of hosts
        """

        hosts = Host.objects.all()
        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)


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
        fields = ("id", "wedding_size", "date", "time",
                  "street_address", "city", "state", "zip_code",
                  "user", "profile_image", "has_happened", "total_costs")


class UpdateHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ("wedding_size", "date", "time",
                  "street_address", "city", "state", "zip_code")
