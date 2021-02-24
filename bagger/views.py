import jwt
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from serializers.serializers import UserSerializer
from model.models import mUser, mUserRegistration
from rest_framework import response
from rest_framework import status
from kwk import settings
from django.contrib import auth
# from decorators.bagger_decorator import role
from permissions.bagger_permission import Bagger_Role
from random import randint

class userRegistration(GenericAPIView, CreateModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Bagger_Role]

    def post(self, requset, *args, **kwargs):
        data = requset.data
        email = data.get('email')
        verification_code = ''
        for _ in range(6):
            verification_code += str(randint(1, 9))
        if email is not None:
            send_mail(
                    'kwk | Verification Code',
                    verification_code,
                    'fitstarproo@gmail.com',
                    [email],
                    fail_silently=False,
                )
            self.create(requset, *args, **kwargs)
            mUserRegistration.objects.create(email=email, verification_code = verification_code)
            
            return response.Response({'Details':'Mail Sent'}, status=status.HTTP_200_OK)

        return response.Response({'Details':'Mail Not Sent'}, status=status.HTTP_400_BAD_REQUEST)


class userLogin(GenericAPIView, CreateModelMixin):

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email','')
        password = data.get('password','')
        user = mUser.objects.get(email= email, password = password)
        if user is not None:
            if user.is_verified == False:
                return response.Response({'details': 'user Not verified'}, status= status.HTTP_403_FORBIDDEN)
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY)
            mSerializer = UserSerializer(user)
            data = {'user': mSerializer.data, 'token': auth_token}
            return response.Response(data, status=status.HTTP_200_OK)
        return response.Response({'details': 'invalid user'}, status= status.status.HTTP_401_UNAUTHORIZED)


class userVerification(GenericAPIView, CreateModelMixin):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        code = data.get('verification_code','')
        if code is not None:
            verificationRec = mUserRegistration.objects.get(verification_code=code)
            if verificationRec is not None:
                user = mUser.objects.get(email = verificationRec.email)
                if user is not None:
                    user.is_verified = True
                    user.save()
                    return response.Response({'details': 'success'}, status= status.status.HTTP_200_OK)
                return response.Response({'details': 'user not found'}, status= status.HTTP_403_FORBIDDEN)
            return response.Response({'details': 'invalid verification code'}, status= status.HTTP_403_FORBIDDEN)
        return response.Response({'details': 'empty code'}, status= status.HTTP_403_FORBIDDEN)
                

class UserList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Bagger_Role]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # @role(allowed_role=['bagger'])
    # def post(self, requset, *args, **kwargs):
    #     return self.create(requset, *args, **kwargs)

# class RUDBagger(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = mUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [Bagger_Role]

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
        
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)