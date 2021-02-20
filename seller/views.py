from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from serializers.serializers import UserSerializer
from model.models import mUser

# Seller views here.
class CreateSeller(GenericAPIView, CreateModelMixin):
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SellerList(GenericAPIView, ListModelMixin):
    queryset = mUser.objects.filter(role="seller")
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveSeller(GenericAPIView, RetrieveModelMixin):
    queryset = mUser.objects.filter(role="seller")
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateSeller(GenericAPIView, UpdateModelMixin):
    queryset = mUser.objects.filter(role="seller")
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteSeller(GenericAPIView, DestroyModelMixin):
    queryset = mUser.objects.filter(role="seller")
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)