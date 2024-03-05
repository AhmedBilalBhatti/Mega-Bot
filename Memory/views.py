from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from Memory.models import Signups


def index(request):
    signup = Signups(username='Ahmed')
    signup.save()

    return render(request,'index.html')
    