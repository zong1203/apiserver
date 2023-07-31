# Create your views here.
from account.models import Userfile,Chathistory
from account.models import search_by_account_raw,jwt_search,account_search
from account.serializers import UserfileSerializer,UserfileSerializer_for_profile

from commodity.models import get_commodity_by_account
from commodity.serializers import CommoditySerializer

from picture.views import upload_image

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import JsonResponse,HttpResponse
from django.shortcuts import render

import json,jwt,datetime,hashlib
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

secret = "zong1203vafnvbiwfjnvbhlifzdv"
# Create your views here.
class UserfileViewSet(viewsets.ModelViewSet):
    queryset = Userfile.objects.all()
    serializer_class = UserfileSerializer

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
        method='post',
        operation_summary='登入用API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account':openapi.Schema(type=openapi.TYPE_STRING,description='帳號'),
                'password':openapi.Schema(type=openapi.TYPE_STRING,description='密碼'),
            }
        ),
        responses={
            200:'"success":True,\n"message":"jwt token",\n"account":"帳號"',
            400:'"success":False,\n"message":"錯誤訊息",\n"account":"帳號"'
        }
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse(status=400,data={"fail":"please use json"})
        result = jwt_search(body["account"],body["password"])
        if result != 'ok':
            return JsonResponse(status=400,data={"success":False,"message":result,"account":body["account"]})
        year, month, date = get_date()
        token = jwt.encode({"username":body["account"],"year":year,"month":month,"date":date}, secret, algorithm='HS256')
        return JsonResponse(status=200,data={"success":True,"message":token,"account":body["account"]})
    
    @swagger_auto_schema(
        method='get',
        operation_summary='驗證token是否過期',
        manual_parameters=[
            openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description='你的JWT token',type=openapi.TYPE_STRING),
        ],
        responses={
            200:'"success":True',
            400:'"success":False'
        }
    )
    @action(detail=False, methods=['get'])
    def verify_token(self, request):
        state, account, message = auth(request)
        if state:
            return JsonResponse(status=400,data={"success":state})
        return JsonResponse(status=200,data={"success":state})
    
    @swagger_auto_schema(
        method='post',
        operation_summary='註冊用API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'account':openapi.Schema(type=openapi.TYPE_STRING,description='帳號'),
                'password':openapi.Schema(type=openapi.TYPE_STRING,description='密碼'),
                'mail':openapi.Schema(type=openapi.TYPE_STRING,description='email地址'),
                'phone':openapi.Schema(type=openapi.TYPE_STRING,description='電話號碼'),
            }
        ),
        responses={
            200:'"success":True,\n"message":"註冊成功"',
            400:'"success":False,\n"message":"錯誤訊息"'
        }
    )
    @action(detail=False, methods=['post'])
    def signup(self, request):
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse(status=400,data={"fail":"please use json"})
        result = account_search(body["account"])
        if result == "帳號已經被註冊":
            return JsonResponse(status=400,data={"success":False,"message":result})
        if "account" in body and "password" in body and "mail" in body and "phone" in body:
            Userfile.objects.create(
                Account = body["account"],
                Password = hashlib.sha256(body["password"].encode('utf-8')).hexdigest(),
                Name = body["account"],
                Email = body["mail"],
                Phonenumber = body["phone"],
                StudentID = "",
                Introduction = "",
                Favorite = "",
                Profliephoto = ""
            )
            result = account_search(body["account"])
            if result == "帳號已經被註冊":
                return JsonResponse(status=200,data={"success":True,"message":"註冊成功"})
            return JsonResponse(status=400,data={"success":False,"message":"註冊失敗"})
        else:
            return JsonResponse(status=400,data={"success":False,"message":"註冊失敗"})

    @swagger_auto_schema(deprecated=True)
    @action(detail=False, methods=['get'])
    def search_by_account(self, request):
        account = request.query_params.get('account', None)
        userfile = Userfile.objects.all().values()
        serializer = UserfileSerializer(userfile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='用來瀏覽賣場以及賣場內的所有商品',
        manual_parameters=[
            openapi.Parameter(
                name='account',
                in_=openapi.IN_QUERY,
                description='賣場名稱',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200:'"success":True\n"provider":商店的基本訊息\n"commodity":商店內的貨物',
            400:'"success":False'
        }
    )
    @action(detail=False, methods=['get'])
    def browse_store(self, request):
        account = request.query_params.get('account', None)
        if not account:
            return JsonResponse(status=400,data={"success":False})
        userfile = search_by_account_raw(account=account)
        provider = {}
        provider["phone"] = userfile[0].Phonenumber
        provider["mail"] = userfile[0].Email
        provider["nickname"] = userfile[0].Name
        provider["intro"] = userfile[0].Introduction
        commodity = get_commodity_by_account(account)
        serializer = CommoditySerializer(commodity, many=True)
        return JsonResponse(status=200,data={"success":True,"provider":provider,"commodity":serializer.data})
    
    @action(detail=False, methods=['post'])
    def password_change(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse(status=400,data={"fail":"please use json"})
        if hashlib.sha256(body["oldPassword"].encode('utf-8')).hexdigest() == Userfile.objects.filter(Account=account)[0].Password:
            if body["oldPassword"] == body["newPassword"]:
                return JsonResponse(status=400,data={"success":False,"message":"新舊密碼不可相同"})
            newpassword_sha256 = hashlib.sha256(body["newPassword"].encode('utf-8')).hexdigest()
            Userfile.objects.filter(Account=account).update(Password=newpassword_sha256)
            return JsonResponse(status=200,data={"success":True,"message":"更改成功"})
        else:
            return JsonResponse(status=400,data={"success":False,"message":"密碼錯誤"})

    @action(detail=False, methods=['get','put'])
    def profile(self, request):
        state, account, state_message = auth(request)
        if state == False:
            return JsonResponse(status=400,data=state_message)
        if request.method == 'GET':
            Account = Userfile.objects.filter(Account=account)
            serializer = UserfileSerializer_for_profile(Account, many=True)
            return JsonResponse(status=200,data={"success":True,"data":serializer.data[0]})
        if request.method == 'PUT':
            body_unicode = request.body.decode('utf-8')
            try:
                body = json.loads(body_unicode)
            except:
                return JsonResponse(status=400,data={"fail":"please use json"})
            for i in body.keys():
                if i == "nickname":
                    Userfile.objects.filter(Account=account).update(Name=body[i])
                if i == "intro":
                    Userfile.objects.filter(Account=account).update(Introduction=body[i])
                if i == "phone":
                    Userfile.objects.filter(Account=account).update(Phonenumber=body[i])
                if i == "mail":
                    Userfile.objects.filter(Account=account).update(Email=body[i])
            return JsonResponse(status=200,data={"success":True})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log(request):
    # if get_client_ip(request=request) != "192.168.0.1":
    #     return render(request, 'log.html', {'sorry': "Sorry,you're not admin"})
    # with open("server.log","r") as f:
    #     text = f.readlines()
    #     text = [i.rstrip() for i in text]
    #     return render(request, 'log.html', {'text': text})
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("123", {
        "type": "chat.message",
        "sender": "system",
        "message": "Hello there!",
    })
    return JsonResponse(status=200,data={"success":True})

def get_date():
    today = datetime.date.today()
    return today.year,today.month,today.day

def auth(request):
    try:
        token = request.headers.get("Authorization")
        payload = jwt.decode(token, secret, algorithms='HS256')
    except:
        return False,None,{"success":False,"message":"authorizate failed"}
    year, month, date = get_date()
    d1 = datetime.date((payload["year"]), (payload["month"]), (payload["date"]))
    d2 = datetime.date(year, month, date)
    if abs(d2-d1).days > 10:
        return False,payload["username"],{"success":False,"message":"jwt time limit exceeded"}
    return True,payload["username"],None
#======================================================================================================
#chathistory
def new_message(sender,receiver,type,content):
    if type == "text":
        now = datetime.datetime.now()

        Chathistory.objects.create(
            Sender = sender,
            Receiver = receiver,
            Type = type,
            Content = content,
            Date = now.strftime('%Y/%m/%d'),
            Time = now.strftime('%H:%M:%S')
        )
    elif type == "picture":
        Chathistory.objects.create(
            Sender = sender,
            Receiver = receiver,
            Type = type,
            Content = upload_image(content),
            Date = now.strftime('%Y/%m/%d'),
            Time = now.strftime('%H:%M:%S')
        )