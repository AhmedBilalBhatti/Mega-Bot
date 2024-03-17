from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('chat/', views.chat, name='chat'),
    path('signup_login/<str:action>', views.signup_login, name='signup_login'),
    path('face_id', views.face_id, name='face_id'),
    path('signout', views.signout, name='signout'),
    path('contact', views.contact, name='contact'),
    path('speech_to_text', views.speech_to_text, name='speech_to_text'),
    path('forgot1', views.forgot1, name='forgot1'),
    path('otpverifcation',views.otpverifcation,name='otpverifcation'),
    path('forgot3',views.forgot3,name='forgot3'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('upload-profile-pic/', views.upload_profile_pic, name='upload-profile-pic'),
]