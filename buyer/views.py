from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from serializers.serializers import UserSerializer
from model.models import mUser

# Buyer views here.
class CreateBuyer(GenericAPIView, CreateModelMixin):
    queryset = mUser.objects.filter(role='buyer')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BuyerList(GenericAPIView, ListModelMixin):
    queryset = mUser.objects.filter(role='buyer')
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveBuyer(GenericAPIView, RetrieveModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateBuyer(GenericAPIView, UpdateModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteBuyer(GenericAPIView, DestroyModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)