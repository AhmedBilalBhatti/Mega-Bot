from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse ,JsonResponse
from .models import *
from Memory.models import Signups


def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import random

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # Process the message here
        # ...
        # Choose a random bot message
        bot_messages = [
            "Hey !!",
            "Can you please send me $20.59 ?",
            "Received it",
            "Can you please share your QR-code ?",
            "Oky..!! ",
            "Thank you..!!",
            "Yes, I’ll sendn",
        ]
        bot_response = random.choice(bot_messages)
        return JsonResponse({'bot_response': bot_response})

    return render(request, 'chat.html')