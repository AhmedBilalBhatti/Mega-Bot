from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from Memory.models import Signups


def index(request):
    signup = Signups(username='example_username', name='AHMED')
    signup.save()

    return render(request,'index.html')
    