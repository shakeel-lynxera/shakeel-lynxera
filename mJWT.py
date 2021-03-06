from django.contrib.auth.models import UserManager
import jwt
from rest_framework import authentication, exceptions
from kwk import settings
from model.models import mUser

class JWTAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(" ")
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            userEmail = mUser.objects.get(email = payload['email'])
            return (userEmail, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Token Expired')
        return super().authenticate(request)
