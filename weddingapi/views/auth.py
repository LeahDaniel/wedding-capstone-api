from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from weddingapi.models import Host, Vendor


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_vendor(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        is_staff=True
    )

    vendor = Vendor.objects.create(
        user=new_user,
        vendor_type_id=request.data['vendor_type_id'],
        business_name=request.data['business_name'],
        city=request.data['city'],
        state=request.data['state'],
        zip_code=request.data['zip_code'],
        description=request.data["description"],
        profile_image=request.data["profile_image"],
        years_in_business=request.data["years_in_business"]
    )

    token = Token.objects.create(user=vendor.user)

    data = {'token': token.key}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_host(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        is_staff=False
    )

    host = Host.objects.create(
        user=new_user,
        wedding_size_id=request.data['wedding_size_id'],
        profile_image=request.data["profile_image"],
        date=request.data["date"],
        time=request.data["time"],
        street_address=request.data['street_address'],
        city=request.data['city'],
        state=request.data['state'],
        zip_code=request.data['zip_code']
    )

    token = Token.objects.create(user=host.user)

    data = {'token': token.key}
    return Response(data)
