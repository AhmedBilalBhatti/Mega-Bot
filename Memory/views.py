from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse ,JsonResponse
from .models import *
from Memory.models import Signups


def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def chat(request):
    if request.method == 'POST':
        messages = request.POST['message']
        print(messages)

    return render(request, 'chat.html')
