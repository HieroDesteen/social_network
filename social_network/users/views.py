import jwt
from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler

from users.models import User
from users.serializers import UserSerializer
from users.utils import ClearbitUserEnrichment


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = ClearbitUserEnrichment(data=request.data)
        serializer = UserSerializer(data=user.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email and password:
        res = {'error': 'Please provide an email and password'}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email, password=password)
    except ObjectDoesNotExist:
        res = {
            'error': 'Can not authenticate with the given credentials or the account has been deactivated'}
        return Response(res, status=status.HTTP_403_FORBIDDEN)
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    user_details = {}
    user_details['name'] = "%s %s" % (
        user.first_name, user.last_name)
    user_details['token'] = token
    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)
    return Response(user_details, status=status.HTTP_200_OK)
