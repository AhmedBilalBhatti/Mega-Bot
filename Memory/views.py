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
        user_message = request.POST.get('message', '')
        if user_message:
            print(user_message)  # This will print the value of the input field to the console
        else:
            print("Not working")

    return render(request, 'chat.html')
