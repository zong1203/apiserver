from django.shortcuts import render
from django.http import HttpResponse
import os
# Create your views here.
def read_img(request):
    try:
        picture_name = request.GET['picture_name']
        imagepath = f"./picture/profile/{picture_name}"
        with open(imagepath, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/jpg")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))