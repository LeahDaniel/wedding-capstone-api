"""View module for handling requests about messages"""
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from weddingapi.models import Message, Host, Vendor
from weddingapi.views.host import HostSerializer
from weddingapi.views.host_vendor import SimpleVendorSerializer


class MessageView(ViewSet):
    """Message view"""

    def list(self, request):
        """Handle GET requests to get all messages

        Returns:
            Response -- JSON serialized list of messages
        """

        vendor_id = request.query_params.get('vendor', None)
        host_id = request.query_params.get('host', None)

        messages = Message.objects.order_by("time_sent")

        if vendor_id is not None:
            vendor = Vendor.objects.get(pk=vendor_id)
            messages = messages.filter(vendor=vendor)

        if host_id is not None:
            host = Host.objects.get(pk=host_id)
            messages = messages.filter(host=host)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized message instance
        """
        try:
            serializer = CreateMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(sender=request.auth.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a message

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            message = Message.objects.get(pk=pk)
            serializer = CreateMessageSerializer(message, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """[summary]

        Args:
            request ([type]): [description]
            pk ([type]): [description]

        Returns:
            [type]: [description]
        """
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path="vendorthreads")
    def get_vendor_threads(self, request):
        """Get most recent messages associated with each message thread"""

        host = Host.objects.get(user=request.auth.user)
        
        messages = Message.objects.raw("""
            SELECT m.id, m.body, m.vendor_id, m.sender_id, m.host_id,
                v.business_name, MAX(m.time_sent)
            FROM weddingapi_message m
            JOIN weddingapi_vendor v ON m.vendor_id = v.id
            WHERE m.host_id IS %s
            GROUP BY vendor_id
            """, (host.id, ))

        serializer = ThreadSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False, url_path="hostthreads")
    def get_host_threads(self, request):
        """Get most recent messages associated with each message thread"""

        vendor = Vendor.objects.get(user=request.auth.user)
        messages = Message.objects.raw("""
            SELECT m.id, m.vendor_id, m.sender_id, m.host_id, m.body,
                u.username host_username, MAX(m.time_sent)
            FROM weddingapi_message m
            JOIN weddingapi_host h ON m.host_id = h.id
            JOIN auth_user u ON h.user_id = u.id
            WHERE m.vendor_id IS %s
            GROUP BY host_id
            """, (vendor.id, ))

        serializer = ThreadSerializer(messages, many=True)
        return Response(serializer.data)


class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer for messages
    """

    class Meta:
        model = Message
        depth= 1
        fields = ('id', 'vendor', 'host', 'body', 'time_sent', 'sender_id')


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('vendor', 'host', 'body')


class ThreadSerializer(serializers.ModelSerializer):
    host = HostSerializer(many=False)
    vendor = SimpleVendorSerializer(many=False)
    
    class Meta:
        model = Message
        fields = ('id','vendor', 'host', 'sender', 'body')
