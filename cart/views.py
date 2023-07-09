from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from cart.models import Cart
from cart.serializers import CartSerializer
from commodity.models import search_by_commodity_raw
from account.views import auth

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

    # @swagger_auto_schema(
    #     method='get',
    #     operation_summary='取得商品資訊(修改用),需使用jwt,並且在網址列加上目標商品的id',
    #     manual_parameters=[
    #         openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
    #         openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
    #     ],
    #     responses={
    #         200:'"success":True,\n"data":商品訊息,',
    #         400:'"success":False,\n"message":"錯誤訊息"'
    #     }
    # )
    # @swagger_auto_schema(
    #     method='post',
    #     operation_summary='上傳商品,圖片為base64傳輸,需使用jwt',
    #     manual_parameters=[
    #         openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
    #     ],
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'name':openapi.Schema(type=openapi.TYPE_STRING,description='商品名稱'),
    #             'launched':openapi.Schema(type=openapi.TYPE_BOOLEAN,description='上下架狀態'),
    #             'description':openapi.Schema(type=openapi.TYPE_STRING,description='商品描述'),
    #             'price':openapi.Schema(type=openapi.TYPE_STRING,description='商品價格'),
    #             'amount':openapi.Schema(type=openapi.TYPE_STRING,description='商品數量'),
    #             'position':openapi.Schema(type=openapi.TYPE_STRING,description='商品位置'),
    #             'image':openapi.Schema(type=openapi.TYPE_STRING,description='商品圖片,至少一張,至多五張,以陣列形式上傳'),
    #         }
    #     ),
    #     responses={
    #         200:'"success":True',
    #         400:'"success":False,\n"message":"錯誤訊息"'
    #     }
    # )
    # @swagger_auto_schema(
    #     method='delete',
    #     operation_summary='刪除商品,需使用jwt,並且在網址列加上目標商品的id',
    #     manual_parameters=[
    #         openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
    #         openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
    #     ],
    #     responses={
    #         200:'"success":True,\n"data":商品訊息,',
    #         400:'"success":False,\n"message":"錯誤訊息"'
    #     }
    # )
    @action(detail=False, methods=['get','post','delete'])
    def cart_CRUD(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        # R
        if request.method == 'GET':
            commodity_id = request.query_params.get('id', None)
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
            cart = Cart.objects.filter(Account=account)
            flag = True
            for i, j  in enumerate(cart):
                if j.Commodity_ID == commodity_id:
                    flag = False
            if flag:
                return JsonResponse(status=200,data={"success":True,"isAdded":False})
            return JsonResponse(status=200,data={"success":True,"isAdded":True})
        # C
        if request.method == 'POST':
            commodity_id = request.query_params.get('id', None)
            if not commodity_id:
                return JsonResponse(status=400,data={"success":False,"message":"Please add parameters to the URL."})
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
            cart = Cart.objects.filter(Account=account)
            for i in cart:
                if commodity_id == i.Commodity_ID:
                    return JsonResponse(status=400,data={"success":False,"message":"Already in your Cart."})
            Cart.objects.create(Account=account,Seller=commodity[0].Account,Commodity_ID=commodity_id)
            return JsonResponse(status=200,data={"success":True})
        # D
        if request.method == 'DELETE':
            commodity_id = request.query_params.get('id', None)
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
            cart = Cart.objects.filter(Account=account)
            flag = True
            for i, j  in enumerate(cart):
                if j.Commodity_ID == commodity_id:
                    flag = False
                    cart[i].delete()
            if flag == True:
                return JsonResponse(status=400,data={"success":False,"message":"This commodity isn't in your Cart"})
            return JsonResponse(status=200,data={"success":True})