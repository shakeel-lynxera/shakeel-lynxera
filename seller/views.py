from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .models import seller
from .serializers import sellerSerializer


@api_view(['GET'])
def index(request):
    return Response('This is buyer view',)


@login_required
@api_view(['GET'])
def add(request):
    sellers = seller.objects.all()
    serialize = sellerSerializer(sellers, many=True)
    return Response(serialize.data)
