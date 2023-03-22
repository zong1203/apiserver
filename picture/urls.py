from django.urls import path,include
from . import views

urlpatterns = [
    path('get/', views.get_image),
    path('upload/', views.upload_image),
]