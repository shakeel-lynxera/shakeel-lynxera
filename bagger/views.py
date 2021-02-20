from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from serializers.serializers import UserSerializer
from model.models import mUser
# Bagger views here.

class CreateBagger(GenericAPIView, CreateModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BaggerList(GenericAPIView, ListModelMixin):
    queryset = mUser.objects.filter(role='bagger')
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveBagger(GenericAPIView, RetrieveModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateBagger(GenericAPIView, UpdateModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteBagger(GenericAPIView, DestroyModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)