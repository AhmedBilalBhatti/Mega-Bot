from django.shortcuts import render,redirect
from django.conf import settings
from Memory.face_id import FaceRecognition
from django.http import HttpResponse ,JsonResponse,HttpResponseBadRequest
from .models import *
from datetime import datetime
from Memory.models import Signups
from MegaBot.settings import BASE_DIR

faceRecognition = FaceRecognition()

def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('index')

def index(request):
    session = request.session.get('user_id')
    return render(request,'index.html')

def login(request):
    return render(request, 'login.html')

    

def signup_login(request, action=None):
    if request.method == "POST":
        if action == 'signup':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            dob_str = request.POST.get('dob')
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponseBadRequest("Invalid date format for date of birth.")
            else:
                return HttpResponseBadRequest("Date of birth is required.")
            user = Signups(username=name, email=email, password=password, dob=dob)
            user.save()
            user_element_id = user.element_id
            if user_element_id[-2] == ":":
                face_id = user_element_id[-1:]
            else:
                face_id = user_element_id[-2:]
            user.uid = face_id
            user.save()
            print("Id===", face_id)
            addFace(face_id)
            return redirect('index')

        else:
            if action == 'login':
                mail = request.POST.get('emailid')
                passcode = request.POST.get('password')
                user = Signups.nodes.get(email=mail, password=password)
                request.session['user_id'] = user.face_id
                if user:
                    return redirect('index')
                else:
                    return HttpResponse('Wrong Email or Password')
                     
    return render(request, 'login.html')

def face_id(request):
    face_id = faceRecognition.recognizeFace()
    try:
        user = Signups.nodes.filter(uid=face_id).get()
        if user:
            request.session['user_id'] = face_id
            return redirect('index')
        else:
            return HttpResponse('Wrong Email or Password')
    except Signups.DoesNotExist:
        return HttpResponse('User not found')

    return redirect ('index')


    
def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message', '') 
        if message:
            print(message)
        
        bot_response = 'hello'
        return JsonResponse({'bot_response': bot_response})

    return render(request, 'chat.html')
