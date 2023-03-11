# Create your views here.
from account.models import Userfile
from account.models import search_by_account_raw,jwt_search,account_search
from account.serializers import UserfileSerializer

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import JsonResponse

import json,jwt,datetime

secret = "zong1203vafnvbiwfjnvbhlifzdv"
# Create your views here.
class UserfileViewSet(viewsets.ModelViewSet):
    queryset = Userfile.objects.all()
    serializer_class = UserfileSerializer

    @action(detail=False, methods=['get'])
    def search_by_account(self, request):
        account = request.query_params.get('account', None)
        userfile = search_by_account_raw(account=account)
        serializer = UserfileSerializer(userfile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
            if abs(d2-d1).days > 15:
                return JsonResponse({"success":False,"account":payload["username"]})
            return JsonResponse({"success":True,"account":payload["username"]})
        except:
            return JsonResponse({"success":False,"account":payload["username"]})
    except:
        return JsonResponse({"success":False,"account":payload["username"]})
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
        Userfile.objects.create(Account = body["account"],
                                Password = body["password"],
                                Name = body["nickname"],
                                Email = body["mail"],
                                Phonenumber = body["phone"],
                                StudentID = "",
                                Introduction = "",
                                Favorite = "",
                                Profliephoto = "")
        result = account_search(body["account"])
        if result == "帳號已經被註冊":
            return JsonResponse({"success":True,"message":"註冊成功"})
        return JsonResponse({"success":False,"message":"註冊失敗"})
# Sign up finish
