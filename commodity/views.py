from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from commodity.models import Commodity,search_by_commodity_raw
from commodity.serializers import CommoditySerializer
from picture.views import upload_commodity_image
from account.views import auth

import json

# Create your views here.
def upload(request):
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
        if 'name' not in body or 'description' not in body or 'price' not in body or 'amount' not in body or 'position' not in body or 'img1' not in body:
            return JsonResponse({"success":False,"message":"缺少必要資料"})
        if 'img2' not in body:
            Commodity.objects.create(
                Launched = True,
                Img1 = upload_commodity_image(body["img1"]),
                Name = body["name"],
                Deacription = body["description"],
                Price = body["price"],
                Amount = body["amount"],
                Position = body["position"],
                Account = account
            )
            return JsonResponse({"success":True,"message":"成功上傳商品"})
        if 'img3' not in body:
            Commodity.objects.create(
                Launched = True,
                Img1 = upload_commodity_image(body["img1"]),
                Img2 = upload_commodity_image(body["img2"]),
                Name = body["name"],
                Deacription = body["description"],
                Price = body["price"],
                Amount = body["amount"],
                Position = body["position"],
                Account = account
            )
            return JsonResponse({"success":True,"message":"成功上傳商品"})
        if 'img4' not in body:
            Commodity.objects.create(
                Launched = True,
                Img1 = upload_commodity_image(body["img1"]),
                Img2 = upload_commodity_image(body["img2"]),
                Img3 = upload_commodity_image(body["img3"]),
                Name = body["name"],
                Deacription = body["description"],
                Price = body["price"],
                Amount = body["amount"],
                Position = body["position"],
                Account = account
            )
            return JsonResponse({"success":True,"message":"成功上傳商品"})
        if 'img5' not in body:
            Commodity.objects.create(
                Launched = True,
                Img1 = upload_commodity_image(body["img1"]),
                Img2 = upload_commodity_image(body["img2"]),
                Img3 = upload_commodity_image(body["img3"]),
                Img4 = upload_commodity_image(body["img4"]),
                Name = body["name"],
                Deacription = body["description"],
                Price = body["price"],
                Amount = body["amount"],
                Position = body["position"],
                Account = account
            )
            return JsonResponse({"success":True,"message":"成功上傳商品"})
        Commodity.objects.create(
            Launched = True,
            Img1 = upload_commodity_image(body["img1"]),
            Img2 = upload_commodity_image(body["img2"]),
            Img3 = upload_commodity_image(body["img3"]),
            Img4 = upload_commodity_image(body["img4"]),
            Img5 = upload_commodity_image(body["img5"]),
            Name = body["name"],
            Deacription = body["description"],
            Price = body["price"],
            Amount = body["amount"],
            Position = body["position"],
            Account = account
        )
        return JsonResponse({"success":True,"message":"成功上傳商品"})
    return JsonResponse({"success":False,"message":"請使用post"})

class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

    @action(detail=False, methods=['get'])
    def search_by_commodity(self, request):
        account = request.query_params.get('account', None)
        userfile = search_by_commodity_raw(account=account)
        serializer = CommoditySerializer(userfile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)