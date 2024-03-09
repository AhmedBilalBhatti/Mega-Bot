from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('chat/', views.chat, name='chat'),
    path('signup_login/<str:action>', views.signup_login, name='signup_login'),
    path('face_id', views.face_id, name='face_id'),
]