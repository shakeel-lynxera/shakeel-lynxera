from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


# Driver views here.
class CreateDriver(GenericAPIView, CreateModelMixin):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DriverList(GenericAPIView, ListModelMixin):
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveDriver(GenericAPIView, RetrieveModelMixin):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateDriver(GenericAPIView, UpdateModelMixin):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteDriver(GenericAPIView, DestroyModelMixin):

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)