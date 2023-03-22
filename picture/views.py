from django.shortcuts import render
from django.http import HttpResponse
import os
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