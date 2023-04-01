from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os,json,base64,uuid
# Create your views here.


def get_image(request):
    try:
        type_name, picture_name = request.GET['type'], request.GET['picture_name']
        imagepath = f"./picture/{type_name}/{picture_name}"
        with open(imagepath, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/jpg")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

def upload_image(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse({"fail":"please use json"})
        if (body["type"] != "profile") and (body["type"] != "commodity"):
            return HttpResponse("type error")
        base64file = base64.b64decode(bytes(body["base64"], 'utf-8'))
        img_file = open(f'./picture/{body["type"]}/{uuid.uuid1()}.jpg', 'wb')
        img_file.write(base64file)
        img_file.close()
        return HttpResponse("ok")
    return HttpResponse('some thing went wrong')

def upload_commodity_image(base64data):
    name = uuid.uuid1()
    base64file = base64.b64decode(bytes(base64data, 'utf-8'))
    img_file = open(f'./picture/commodity/{name}.jpg', 'wb')
    img_file.write(base64file)
    img_file.close()
    return name
    