from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('login', views.login, name='login'),
    path('signup_login', views.signup_login, name='signup_login'),
]