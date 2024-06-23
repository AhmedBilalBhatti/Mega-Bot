from django.urls import path
from . import views

urlpatterns = [
    path('drone_video_feed/',views.drone_video_feed, name='drone_video_feed'),
    path('take_picture/',views.take_picture, name='take_picture'),
]