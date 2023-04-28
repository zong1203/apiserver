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

import json

# Create your views here.

class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

    @action(detail=False, methods=['get'])
    def search_by_commodity(self, request):
        commodity = request.query_params.get('commodity', None)
        userfile = search_by_commodity_raw(commodity=commodity)
        serializer = CommoditySerializer(userfile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get','post','put','delete'])
    def commodity_CRUD(self, request):
        # if request.method == 'GET':
        #     try:
        #         headers = request.headers.get("Authorization")
        #     except:
        #         return JsonResponse({"success":False,"message":"please authorizate"})
        #     state, account = auth(headers)
        #     if state == False:
        #         return JsonResponse({"success":False,"message":"json time limit exceeded"})
            
        if request.method == 'POST':
            try:
                headers = request.headers.get("Authorization")
            except:
                return JsonResponse({"success":False,"message":"please authorizate"})
            state, account = auth(headers)
            if state == False:
                return JsonResponse({"success":False,"message":"json time limit exceeded"})
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse({"fail":"please use json"})
            if 'name' not in body or 'description' not in body or 'price' not in body or 'amount' not in body or 'position' not in body or 'image' not in body:
                return JsonResponse({"success":False,"message":"缺少必要資料"})
            img = ["","","","",""]
            for i, j in enumerate(body["image"]):
                img[i] = upload_image(j)
            Commodity.objects.create(
                Launched = True,
                Img1 = img[0],
                Img2 = img[1],
                Img3 = img[2],
                Img4 = img[3],
                Img5 = img[4],
                Name = body["name"],
                Deacription = body["description"],
                Price = body["price"],
                Amount = body["amount"],
                Position = body["position"],
                Account = account
            )
            return JsonResponse({"success":True,"message":"ok"})