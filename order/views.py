from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.views import auth
from commodity.models import get_price_by_id, get_launch_state_by_ID, get_amount_by_id, reduce_commodity_amount, get_provider_by_commodity_id
from order.serializer import OrderSerializer
from order.models import Order

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import json
import uuid

# Create your views here.


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(auto_schema=None)
    def create(self, request):
        return JsonResponse({"success": False})

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request):
        return JsonResponse({"success": False})

    @swagger_auto_schema(auto_schema=None)
    def update(self, request):
        return JsonResponse({"success": False})

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request):
        return JsonResponse({"success": False})

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request):
        return JsonResponse({"success": False})

    @action(detail=False, methods=['get', 'post', 'put'])
    def order_CRUD(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400, data=state_message)
        # C
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse(status=400, data={"fail": "please use json"})
            if "options" not in body or "comment" not in body or "order" not in body:
                return JsonResponse(status=400, data={"success": False, "message": "缺少必要資料"})
            total_price = 0
            for commodity_id in body["order"]:
                if not get_launch_state_by_ID(commodity_id):
                    return JsonResponse(status=400, data={"success": False, "message": "訂單包含已下架商品，請更新頁面後重試"})
                if (body["order"][commodity_id]["price"]) != get_price_by_id(commodity_id):
                    return JsonResponse(status=400, data={"success": False, "message": "商品金額錯誤，請更新頁面後重試"})
                if (body["order"][commodity_id]["amount"]) > get_amount_by_id(commodity_id):
                    return JsonResponse(status=400, data={"success": False, "message": "商品數量大於庫存，請重新下單"})
            for commodity_id in body["order"]:
                total_price += int(body["order"][commodity_id]["price"]) * int(body["order"][commodity_id]["amount"])
                reduce_commodity_amount(commodity_id,(body["order"][commodity_id]["amount"]))
            Order.objects.create(
                Order_ID=uuid.uuid1(),Consumer=account,Provider=get_provider_by_commodity_id(commodity_id),
                Order=body["order"],Totalprice=total_price,Comment=body["comment"],Options=body["options"],
                Selected_Option={"start":"","end":"","position":""},Using_Message=False,
                Actual={"start":"","end":""},Progress=0
            )
            return JsonResponse(status=200, data={"success": True})
