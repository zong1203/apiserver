from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from commodity.models import Commodity,search_by_commodity_raw
from commodity.serializers import CommoditySerializer
from picture.views import upload_image
from account.views import auth

import json,os

# Create your views here.

class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

    @action(detail=False, methods=['get'])
    def search_by_commodity(self, request):
        commodity_name = request.query_params.get('commodity', None)
        commodity = search_by_commodity_raw(commodity=commodity_name)
        serializer = CommoditySerializer(commodity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_commodity(self, request):
        try:
            headers = request.headers.get("Authorization")
        except:
            return JsonResponse({"success":False,"message":"please authorizate"})
        state, account = auth(headers)
        if state == False:
            return JsonResponse({"success":False,"message":"json time limit exceeded"})
        commodity = Commodity.objects.filter(Account=account).values()
        launched = []
        unlaunched = []
        for i in commodity:
            if i["Launched"]:
                launched.append(i)
            else:
                unlaunched.append(i)
        return JsonResponse({"success":True,"launched":launched,"unlaunched":unlaunched})
    
    @action(detail=False, methods=['post'])
    def launch(self, request):
        try:
            headers = request.headers.get("Authorization")
        except:
            return JsonResponse({"success":False,"message":"please authorizate"})
        state, account = auth(headers)
        if state == False:
            return JsonResponse({"success":False,"message":"json time limit exceeded"})
        commodity_id = request.query_params.get('id', None)
        commodity = search_by_commodity_raw(commodity_id=commodity_id)
        if not commodity:
            return JsonResponse({"success":False,"message":"can't find commodity with this id"})
        if account != commodity[0].Account:
            return JsonResponse({"success":False,"message":"this commodity is not yours"})
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except:
            return JsonResponse({"fail":"please use json"})
        try:
            launched = body["launched"]
        except:
            return JsonResponse({"fail":"can't find 'launched' in body"})
        Commodity.objects.filter(id=int(commodity_id)).update(Launched = launched)
        return JsonResponse({"success":True,"message":"ok"})
        
    
    @action(detail=False, methods=['get','post','put','delete'])
    def commodity_CRUD(self, request):
        try:
            headers = request.headers.get("Authorization")
        except:
            return JsonResponse({"success":False,"message":"please authorizate"})
        state, account = auth(headers)
        if state == False:
            return JsonResponse({"success":False,"message":"json time limit exceeded"})
        # R
        if request.method == 'GET':
            commodity_id = request.query_params.get('id', None)
            if not commodity_id:
                return JsonResponse({"success":False,"message":"Please add parameters to the URL."})
            commodity = Commodity.objects.filter(id=commodity_id).values()
            if not commodity:
                return JsonResponse({"success":False,"message":"can't find commodity with this id"})
            if account != commodity[0]["Account"]:
                return JsonResponse({"success":False,"message":"this commodity is not yours"})
            return JsonResponse({"success":True,"info":commodity[0]})
        
        # C
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse({"fail":"please use json"})
            if 'name' not in body or 'launched' not in body or 'description' not in body or 'price' not in body or 'amount' not in body or 'position' not in body or 'image' not in body:
                return JsonResponse({"success":False,"message":"缺少必要資料"})
            img = ["","","","",""]
            for i, j in enumerate(body["image"]):
                img[i] = upload_image(j)
            Commodity.objects.create(
                Launched = body["launched"],Img1 = img[0],Img2 = img[1],Img3 = img[2],Img4 = img[3],
                Img5 = img[4],Name = body["name"],Deacription = body["description"],Price = body["price"],
                Amount = body["amount"],Position = body["position"],Account = account
            )
            return JsonResponse({"success":True,"message":"ok"})
        
        # U
        if request.method == 'PUT':
            commodity_id = request.query_params.get('id', None)
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse({"success":False,"message":"can't find commodity with this id"})
            if account != commodity[0].Account:
                return JsonResponse({"success":False,"message":"this commodity is not yours"})
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse({"fail":"please use json"})
            if 'name' not in body or 'launched' not in body or 'description' not in body or 'price' not in body or 'amount' not in body or 'position' not in body:
                return JsonResponse({"success":False,"message":"缺少必要資料"})
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
                Img5 = img[4],Name = body["name"],Deacription = body["description"],Price = body["price"],
                Amount = body["amount"],Position = body["position"],Account = account
            )
            return JsonResponse({"success":True,"message":"ok"})
            
        # D
        if request.method == 'DELETE':
            commodity_id = request.query_params.get('id', None)
            commodity = search_by_commodity_raw(commodity_id=commodity_id)
            if not commodity:
                return JsonResponse({"success":False,"message":"can't find commodity with this id"})
            if account != commodity[0].Account:
                return JsonResponse({"success":False,"message":"this commodity is not yours"})
            img = [commodity[0].Img1,commodity[0].Img2,commodity[0].Img3,commodity[0].Img4,commodity[0].Img5]
            for i in img:
                if i:
                    os.remove(f'./picture/picture/{i}')
            commodity[0].delete()
            return JsonResponse({"success":True})