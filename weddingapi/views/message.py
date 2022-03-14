"""View module for handling requests about messages"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from weddingapi.models import Message


class MessageView(ViewSet):
    """Message view"""

    def list(self, request):
        """Handle GET requests to get all messages

        Returns:
            Response -- JSON serialized list of messages
        """

        user = request.auth.user

        messages = Message.objects.filter(Q(sender=user) | Q(
            recipient=user)).order_by('-time_sent')

        vendor_id = request.query_params.get('vendor', None)
        vendor = User.objects.get(vendor_user__id=vendor_id)
        
        host_id = request.query_params.get('host', None)
        host = User.objects.get(host_user__id=host_id)

        if vendor is not None:
            messages = messages.filter(Q(sender=vendor) | Q(
                recipient=vendor))
            
        if host is not None:
            messages = messages.filter(Q(sender=host) | Q(
                recipient=host))

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized message instance
        """
        user=request.auth.user
        try:
            serializer = CreateMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(sender=user)
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



class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer for messages
    """
    
    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'body', 'time_sent')


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('recipient', 'body')
