from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from cart.models import Cart
from cart.serializers import CartSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

    @swagger_auto_schema(auto_schema=None)
    def create(self, request):
        return JsonResponse({"success":False})
    
    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request):
        return JsonResponse({"success":False})

    @swagger_auto_schema(auto_schema=None)
    def update(self, request):
        return JsonResponse({"success":False})
    
    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request):
        return JsonResponse({"success":False})
    
    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request):
        return JsonResponse({"success":False})
