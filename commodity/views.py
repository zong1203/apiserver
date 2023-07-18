from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from commodity.models import Commodity,search_by_commodity_raw,search_by_commodity_keyword
from commodity.serializers import CommoditySerializer
from picture.views import upload_image
from account.views import auth

import json,os

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    

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

    @swagger_auto_schema(
        operation_summary='取得單一商品資訊,需在query加上id',
        manual_parameters=[
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'success":True,\n"commodity":商品資訊',
            400:'success":False,\n"commodity":[]'
        }
    )
    @action(detail=False, methods=['get'])
    def get_commodity(self, request):
        commodity_id = request.query_params.get('id', None)
        if not commodity_id:
            return JsonResponse(status=400,data={"success":False,"commodity":[]})
        commodity = search_by_commodity_raw(commodity_id=commodity_id)
        serializer = CommoditySerializer(commodity, many=True)
        if not serializer.data[0]["Launched"]:
            return JsonResponse(status=400,data={"success":False,"commodity":[]})
        return Response(status=200,data={"success":True,"commodity":serializer.data[0]})
    
    @swagger_auto_schema(
        operation_summary='主頁取得商品用,不需要帶參數',
        responses={
            200:'"data":[全部商品]',
        }
    )
    @action(detail=False, methods=['get'])
    def get_launched_commodity(self, request):
        commodity = search_by_commodity_raw(launched = True)
        serializer = CommoditySerializer(commodity, many=True)
        return Response(status=200,data=serializer.data)
    
    @swagger_auto_schema(
        operation_summary='搜尋商品用,格式為"/api/commodity/get_searched_commodity/?keyword=商品關鍵字"',
        manual_parameters=[
            openapi.Parameter(name='keyword',in_=openapi.IN_QUERY, description='商品keyword',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'"data":[搜尋結果]',
        }
    )
    @action(detail=False, methods=['get'])
    def get_searched_commodity(self, request):
        keyword = request.query_params.get('keyword', None)
        commodity = search_by_commodity_keyword(keyword)
        serializer = CommoditySerializer(commodity, many=True)
        return Response(status=200,data=serializer.data)

    @swagger_auto_schema(deprecated=True)
    @action(detail=False, methods=['get'])
    def search_by_commodity(self, request):
        commodity_name = request.query_params.get('commodity', None)
        commodity = search_by_commodity_raw(commodity=commodity_name)
        serializer = CommoditySerializer(commodity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='取得這個帳號的所有商品(編輯用),需使用jwt',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'"success":True,\n"launched":上架的商品,\n"unlaunched":未上架的商品',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @action(detail=False, methods=['get'])
    def my_commodity(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        commodity = search_by_commodity_raw(account=account)
        serializer = CommoditySerializer(commodity, many=True)
        launched = []
        unlaunched = []
        for i in serializer.data:
            if i["Launched"]:
                launched.append(i)
            else:
                unlaunched.append(i)
        return JsonResponse(status=200,data={"success":True,"launched":launched,"unlaunched":unlaunched})
    
    @swagger_auto_schema(
        operation_summary='更改商品上下架狀態,需使用jwt,並且在網址列加上目標商品的id,格式為"/api/commodity/launch/?id=商品id"',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'launched':openapi.Schema(type=openapi.TYPE_BOOLEAN,description='上下架狀態')
            }
        ),
        responses={
            200:'"success":True',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @action(detail=False, methods=['post'])
    def launch(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        commodity_id = request.query_params.get('id', None)
        commodity = search_by_commodity_raw(commodity_id=commodity_id)
        if not commodity:
            return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
        if account != commodity[0].Account:
            return JsonResponse(status=400,data={"success":False,"message":"this commodity is not yours"})
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except:
            return JsonResponse(status=400,data={"fail":"please use json"})
        try:
            launched = body["launched"]
        except:
            return JsonResponse(status=400,data={"fail":"can't find 'launched' in body"})
        Commodity.objects.filter(id=int(commodity_id)).update(Launched = launched)
        return JsonResponse(status=200,data={"success":True})      
    
    @swagger_auto_schema(
        method='get',
        operation_summary='取得商品資訊(修改用),需使用jwt,並且在網址列加上目標商品的id',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'"success":True,\n"data":商品訊息,',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @swagger_auto_schema(
        method='post',
        operation_summary='上傳商品,圖片為base64傳輸,需使用jwt',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name':openapi.Schema(type=openapi.TYPE_STRING,description='商品名稱'),
                'launched':openapi.Schema(type=openapi.TYPE_BOOLEAN,description='上下架狀態'),
                'description':openapi.Schema(type=openapi.TYPE_STRING,description='商品描述'),
                'price':openapi.Schema(type=openapi.TYPE_STRING,description='商品價格'),
                'amount':openapi.Schema(type=openapi.TYPE_STRING,description='商品數量'),
                'position':openapi.Schema(type=openapi.TYPE_STRING,description='商品位置'),
                'image':openapi.Schema(type=openapi.TYPE_STRING,description='商品圖片,至少一張,至多五張,以陣列形式上傳'),
            }
        ),
        responses={
            200:'"success":True',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @swagger_auto_schema(
        method='put',
        operation_summary='修改商品,圖片為base64傳輸,需使用jwt,並且在網址列加上目標商品的id',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name':openapi.Schema(type=openapi.TYPE_STRING,description='商品名稱'),
                'launched':openapi.Schema(type=openapi.TYPE_BOOLEAN,description='上下架狀態'),
                'description':openapi.Schema(type=openapi.TYPE_STRING,description='商品描述'),
                'price':openapi.Schema(type=openapi.TYPE_STRING,description='商品價格'),
                'amount':openapi.Schema(type=openapi.TYPE_STRING,description='商品數量'),
                'position':openapi.Schema(type=openapi.TYPE_STRING,description='商品位置'),
                'image':openapi.Schema(type=openapi.TYPE_STRING,description='新上傳的商品圖片,至少一張,至多五張,以陣列形式上傳'),
                'remain_image':openapi.Schema(type=openapi.TYPE_STRING,description='要保留下來的圖片檔名,以陣列形式上傳'),
            }
        ),
        responses={
            200:'"success":True',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @swagger_auto_schema(
        method='delete',
        operation_summary='刪除商品,需使用jwt,並且在網址列加上目標商品的id',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
            openapi.Parameter(name='id',in_=openapi.IN_QUERY,description='商品id',type=openapi.TYPE_STRING)
        ],
        responses={
            200:'"success":True,\n"data":商品訊息,',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @action(detail=False, methods=['get','post','put','delete'])
    def commodity_CRUD(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        # R
        if request.method == 'GET':
            commodity_id = request.query_params.get('id', None)
            if not commodity_id:
                return JsonResponse(status=400,data={"success":False,"message":"Please add parameters to the URL."})
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
            if account != commodity[0].Account:
                return JsonResponse(status=400,data={"success":False,"message":"this commodity is not yours"})
            serializer = CommoditySerializer(commodity, many=True)
            return JsonResponse(status=200,data={"success":True,"data":serializer.data[0]})
        
        # C
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse(status=400,data={"fail":"please use json"})
            if 'name' not in body or 'launched' not in body or 'description' not in body or 'price' not in body or 'amount' not in body or 'position' not in body or 'image' not in body:
                return JsonResponse(status=400,data={"success":False,"message":"缺少必要資料"})
            img = ["","","","",""]
            for i, j in enumerate(body["image"]):
                img[i] = upload_image(j)
            Commodity.objects.create(
                Launched = body["launched"],Img1 = img[0],Img2 = img[1],Img3 = img[2],Img4 = img[3],
                Img5 = img[4],Name = body["name"],Description = body["description"],Price = body["price"],
                Amount = body["amount"],Position = body["position"],Account = account
            )
            return JsonResponse(status=200,data={"success":True})
        
        # U
        if request.method == 'PUT':
            commodity_id = request.query_params.get('id', None)
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
            if account != commodity[0].Account:
                return JsonResponse(status=400,data={"success":False,"message":"this commodity is not yours"})
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse(status=400,data={"fail":"please use json"})
            if 'name' not in body or 'launched' not in body or 'description' not in body or 'price' not in body or 'amount' not in body or 'position' not in body:
                return JsonResponse(status=400,data={"success":False,"message":"缺少必要資料"})
            img = [commodity[0].Img1,commodity[0].Img2,commodity[0].Img3,commodity[0].Img4,commodity[0].Img5]
            for i in img:
                if (i not in body["remain_image"]) and i != "":
                    os.remove(f'./picture/picture/{i}')
            img = body["remain_image"]
            for i in body["image"]:
                img.append(upload_image(i))
            while len(img) < 5:
                img.append("")
            Commodity.objects.filter(id=int(commodity_id)).update(
                Launched = body["launched"],Img1 = img[0],Img2 = img[1],Img3 = img[2],Img4 = img[3],
                Img5 = img[4],Name = body["name"],Description = body["description"],Price = body["price"],
                Amount = body["amount"],Position = body["position"],Account = account
            )
            return JsonResponse(status=200,data={"success":True})
            
        # D
        if request.method == 'DELETE':
            commodity_id = request.query_params.get('id', None)
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse(status=400,data={"success":False,"message":"can't find commodity with this id"})
            if account != commodity[0].Account:
                return JsonResponse(status=400,data={"success":False,"message":"this commodity is not yours"})
            img = [commodity[0].Img1,commodity[0].Img2,commodity[0].Img3,commodity[0].Img4,commodity[0].Img5]
            for i in img:
                if i:
                    os.remove(f'./picture/picture/{i}')
            commodity[0].delete()
            return JsonResponse(status=200,data={"success":True})