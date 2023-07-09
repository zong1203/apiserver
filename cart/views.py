from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from cart.models import Cart
from cart.serializers import CartSerializer
from commodity.models import search_by_commodity_raw,get_first_picture,get_launch_state_by_ID
from account.views import auth
from account.models import get_nickname_by_account

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

    @action(detail=False, methods=['get'])
    def my_storecart(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        cart = Cart.objects.filter(Account=account)
        seller = request.query_params.get('seller', None)
        data = []
        for i in cart:
            if (i.Seller == seller) and get_launch_state_by_ID(i.Commodity_ID):
                commodity = search_by_commodity_raw(commodity_id=i.Commodity_ID)
                temp = {}
                temp["id"] = commodity[0].id
                temp["name"] = commodity[0].Name
                temp["cover"] = "image/get/?picture_name="+commodity[0].Img1
                temp["price"] = commodity[0].Price
                temp["amount"] = commodity[0].Amount
                data.append(temp)
        return JsonResponse(status=200,data={"success":True,"result":data})

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        cart = Cart.objects.filter(Account=account)
        seller_list = []
        data = {}
        for i in cart:
            if (i.Seller not in seller_list) and (get_launch_state_by_ID(i.Commodity_ID)):
                seller_list.append(i.Seller)
        for i in seller_list:
            data[i] = {}
            data[i]["nickname"] = get_nickname_by_account(i)
            data[i]["cover"] = ""
            data[i]["items"] = []
            first_commodity = True
            commodity_counter = 0
            for j in cart:
                if j.Seller == i:
                    if first_commodity:
                        data[i]["cover"] = get_first_picture(j.Commodity_ID)
                        first_commodity = False
                    if (get_launch_state_by_ID(j.Commodity_ID)) and (commodity_counter < 4):
                        data[i]["items"].append(j.Commodity_Name)
                        commodity_counter+=1
        return JsonResponse(status=200,data={"success":True,"result":data})

    @swagger_auto_schema(
        method='get',
        operation_summary='確認商品是否存在於購物車內,在網址列加上商品id,並且使用jwt token',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'"success":True,\n"isAdded":是否存在於購物車內,',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @swagger_auto_schema(
        method='post',
        operation_summary='將特定商品新增到購物車內,在網址列加上商品id,並且使用jwt token',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            }
        ),
        responses={
            200:'"success":True',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @swagger_auto_schema(
        method='delete',
        operation_summary='將特定商品從購物車內移除,在網址列加上商品id,並且使用jwt token',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'"success":True',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
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
            Cart.objects.create(Account=account,Seller=commodity[0].Account,Commodity_ID=commodity_id,Commodity_Name=commodity[0].Name)
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