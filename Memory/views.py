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
    bot_resp = "Hello"
    print('bdvhbds')
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if user_message:
            print(user_message)
        else:
            print("Not working")
    

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message:
            print(message)
            response_data = {'status': 'success', 'message': message}
        else:
            response_data = {'status': 'error', 'message': 'No message received'}
    else:
        response_data = {'status': 'error', 'message': 'Invalid request method'}

    return render(request, 'chat.html')



def signup_login(request):
    return render(request,'login.html')