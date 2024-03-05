from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from .models import *
from Memory.models import Signups


def index(request):
    return render(request,'index.html')

def chat(request):
    return render(request,'chat.html')

def login(request):
    return render(request,'login.html')