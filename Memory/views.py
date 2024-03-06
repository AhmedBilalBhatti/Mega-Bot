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
        message = request.POST.get('message', '')
        print(message)
        bot_response = "Hello"
        return JsonResponse({'response': bot_response})

    return render(request, 'chat.html')