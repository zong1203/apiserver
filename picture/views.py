from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os,json,base64,uuid
# Create your views here.


def get_image(request):
    try:
        picture_name = request.GET['picture_name']
        imagepath = f"./picture/picture/{picture_name}"
        with open(imagepath, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/jpg")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

def upload_test_image(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try:
            body = json.loads(body_unicode)
        except:
            return JsonResponse({"fail":"please use json"})
        base64file = base64.b64decode(bytes(body["base64"], 'utf-8'))
        img_file = open(f'./picture/picture/{uuid.uuid1()}.jpg', 'wb')
        img_file.write(base64file)
        img_file.close()
        return HttpResponse("ok")
    return HttpResponse('some thing went wrong')

def upload_image(base64data):
    base64data = base64data.split(";base64,")
    base64data[0] = base64data[0].replace("data:image/","")
    name = str(uuid.uuid1()) + "." + base64data[0]
    base64file = base64.b64decode(bytes(base64data[1], 'utf-8'))
    img_file = open(f'./picture/picture/{name}', 'wb')
    img_file.write(base64file)
    img_file.close()
    return name
    