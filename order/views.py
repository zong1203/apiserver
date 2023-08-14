from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.views import auth
from account.models import get_primary_info_by_name
from commodity.models import get_price_by_id, get_launch_state_by_ID, get_amount_by_id, reduce_commodity_amount, get_provider_by_commodity_id
from order.serializer import OrderSerializer
from order.models import Order,get_order_overview

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import json
import uuid
import datetime

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

    @action(detail=False, methods=['get'])
    def overview(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400, data=state_message)
        order_progress = int(request.query_params.get('progress', None))
        order_status = request.query_params.get('status', None)
        if not (order_status == "consumer" or order_status == "provider"):
            return JsonResponse(status=400, data={"success": False,"message": "參數錯誤"})
        orders = get_order_overview(order_progress,order_status,account)
        return JsonResponse(status=200, data={"success": True,"orders": orders})

    @action(detail=False, methods=['get', 'post', 'put','delete'])
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
                if get_provider_by_commodity_id(commodity_id)==account:
                    return JsonResponse(status=400, data={"success": False, "message": "無法購買自己的商品"})
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
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(get_provider_by_commodity_id(commodity_id), {
                "type": "chat.message",
                "sender": "system",
                "message": "你有一筆新訂單，請盡速查看!",
            })
            return JsonResponse(status=200, data={"success": True})
        
        if request.method == 'GET':
            order_id = request.query_params.get('id', None)
            order = Order.objects.filter(id=order_id)
            serializer = OrderSerializer(order, many=True)
            return JsonResponse(status=200, data={"success": True,"order": serializer.data[0]})
        
        if request.method == 'PUT':
            order_id = request.query_params.get('id', None)
            mode = request.query_params.get('mode', None)
            order = Order.objects.filter(id=order_id)
            if not order:
                return JsonResponse(status=400, data={"success": False, "message": "訂單不存在"})
            if order[0].Progress == 0:#從這邊開始是在剛下訂單的時候的確認訂單
                if mode == '1':
                    body_unicode = request.body.decode('utf-8')
                    try:
                        body = json.loads(body_unicode)
                    except:
                        return JsonResponse(status=400, data={"fail": "please use json"})
                    if "usingMessage" not in body or "selectedOption" not in body:
                        return JsonResponse(status=400, data={"success": False, "message": "缺少必要資料"})
                    if account != order[0].Provider:
                        return JsonResponse(status=400, data={"success": False,"message":"拒絕不符權限的操作"})
                    if body["usingMessage"]:
                        Order.objects.filter(id=order_id).update(Progress=1,Using_Message=True)
                        return JsonResponse(status=200, data={"success": True})
                    if body["selectedOption"]["start"] not in order[0].Options["start"] or body["selectedOption"]["end"] not in order[0].Options["end"] or body["selectedOption"]["position"] not in order[0].Options["position"]:
                        return JsonResponse(status=400, data={"success": False,"message":"選擇的時間或地點不在選項內"})
                    Order.objects.filter(id=order_id).update(Progress=1,Selected_Option=body["selectedOption"])
                    return JsonResponse(status=200, data={"success": True})#到這邊為止是在剛下訂單的時候的確認訂單
                if mode == '2':
                    if not (account == order[0].Provider or account == order[0].Consumer):#從這邊開始是在剛下訂單的時候的取消訂單
                        return JsonResponse(status=400, data={"success": False,"message":"拒絕不符權限的操作"})
                    Order.objects.filter(id=order_id).update(Progress=-1)
                    return JsonResponse(status=200, data={"success": True})#到這邊為止是在剛下訂單的時候的取消訂單
            if order[0].Progress == 1:
                if mode == '2':
                    if not (account == order[0].Provider or account == order[0].Consumer):#從這邊開始是在交貨前的取消訂單
                        return JsonResponse(status=400, data={"success": False,"message":"拒絕不符權限的操作"})
                    Order.objects.filter(id=order_id).update(Progress=-1)
                    return JsonResponse(status=200, data={"success": True})#到這邊為止是在交貨前的取消訂單
                if mode == '3':#從這邊開始是在交貨前的確認收到貨
                    if account != order[0].Consumer:
                        return JsonResponse(status=400, data={"success": False,"message":"拒絕不符權限的操作"})
                    now = datetime.datetime.now()
                    actual = {
                        "start": now.strftime('20%y-%m-%dT%H:%M'),
                        "end": ""
                    }
                    Order.objects.filter(id=order_id).update(Progress=2,Actual=actual)
                    return JsonResponse(status=200, data={"success": True})#到這邊為止是在交貨前的確認收到貨
            if order[0].Progress == 2:#從這邊開始是在歸還前的確認領回貨
                if mode == '4':
                    if account != order[0].Provider:
                        return JsonResponse(status=400, data={"success": False,"message":"拒絕不符權限的操作"})
                    actual = order[0].Actual
                    now = datetime.datetime.now()
                    actual["end"] = now.strftime('20%y-%m-%dT%H:%M')
                    Order.objects.filter(id=order_id).update(Progress=3,Actual=actual)
                    return JsonResponse(status=200, data={"success": True})#到這邊為止是在歸還前的確認領回貨
            return JsonResponse(status=200, data={"success": False,"message": "此階段無法進行此操作"})
        
        if request.method == 'DELETE':
            # order_id = request.query_params.get('id', None)
            # Order.objects.filter(id=order_id).delete()
            return JsonResponse(status=200, data={"success": True})