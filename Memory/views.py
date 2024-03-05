from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from .models import *
from Memory.models import Signups


def index(request):
    Signups(username='Ahmed').save()

    return render(request,'index.html')
    