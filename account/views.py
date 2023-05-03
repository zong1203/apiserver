# Create your views here.
from account.models import Userfile,Chathistory
from account.models import search_by_account_raw,jwt_search,account_search
from account.serializers import UserfileSerializer

from commodity.models import get_commodity_by_account
from commodity.serializers import CommoditySerializer

from picture.views import upload_image

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import JsonResponse,HttpResponse
from django.shortcuts import render

import json,jwt,datetime,hashlib

secret = "zong1203vafnvbiwfjnvbhlifzdv"
# Create your views here.
class UserfileViewSet(viewsets.ModelViewSet):
    queryset = Userfile.objects.all()
    serializer_class = UserfileSerializer

    def create(self, request):
        return JsonResponse({"success":False})
    
    def retrieve(self, request):
        return JsonResponse({"success":False})

    def update(self, request):
        return JsonResponse({"success":False})

    @action(detail=False, methods=['get'])
    def search_by_account(self, request):
        account = request.query_params.get('account', None)
        userfile = Userfile.objects.all().values()
        serializer = UserfileSerializer(userfile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def browse_store(self, request):
        account = request.query_params.get('account', None)
        userfile = search_by_account_raw(account=account)
        if not userfile:
            return JsonResponse({"success":False})
        provider = {}
        provider["phone"] = userfile[0].Phonenumber
        provider["mail"] = userfile[0].Email
        provider["nickname"] = userfile[0].Name
        provider["intro"] = userfile[0].Introduction
        commodity = get_commodity_by_account(account)
        serializer = CommoditySerializer(commodity, many=True)
        return JsonResponse({"success":True,"provider":provider,"commodity":serializer.data})
    
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
    with open("server.log","r") as f:
        text = f.readlines()
        text = [i.rstrip() for i in text]
        return render(request, 'log.html', {'text': text})
# JWT token
def get_date():
    today = datetime.date.today()
    return today.year,today.month,today.day

def get_token(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse({"fail":"please use json"})
        result = jwt_search(body["account"],body["password"])
        if result != 'ok':
            return JsonResponse({"success":False,"message":result,"account":body["account"]})
        year, month, date = get_date()
        token = jwt.encode({"username":body["account"],"password":body["password"],"year":year,"month":month,"date":date}, secret, algorithm='HS256')
        return JsonResponse({"success":True,"message":token,"account":body["account"]})
    else:
        return JsonResponse({"fail":"please use post method"})

def verify_token(request):
    try:
        headers = request.headers.get("Authorization")
        try:
            payload = jwt.decode(headers, secret, algorithms='HS256')
            year, month, date = get_date()
            d1 = datetime.date((payload["year"]), (payload["month"]), (payload["date"]))
            d2 = datetime.date(year, month, date)
            if abs(d2-d1).days > 10:
                return JsonResponse({"success":False,"account":payload["username"]})
            return JsonResponse({"success":True,"account":payload["username"]})
        except:
            return JsonResponse({"success":False,"account":payload["username"]})
    except:
        return JsonResponse({"success":False,"account":payload["username"]})

def auth(token):
    payload = jwt.decode(token, secret, algorithms='HS256')
    year, month, date = get_date()
    d1 = datetime.date((payload["year"]), (payload["month"]), (payload["date"]))
    d2 = datetime.date(year, month, date)
    if abs(d2-d1).days > 10:
        return False,payload["username"]
    return True,payload["username"]
# JWT token finish
# Sign up
def sign_up(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse({"fail":"please use json"})
        result = account_search(body["account"])
        if result == "帳號已經被註冊":
            return JsonResponse({"success":False,"message":result})
        print(body)
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
                return JsonResponse({"success":True,"message":"註冊成功"})
            return JsonResponse({"success":False,"message":"註冊失敗"})
        else:
            return JsonResponse({"success":False,"message":"註冊失敗"})
# Sign up finish
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