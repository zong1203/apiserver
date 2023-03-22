from django.urls import path,include
from . import views

urlpatterns = [
    path('login/', views.get_token),
    path('token_verify/', views.verify_token),
    path('signup/', views.sign_up),
]