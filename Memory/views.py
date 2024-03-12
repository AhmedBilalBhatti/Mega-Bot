from django.http import HttpResponse ,JsonResponse,HttpResponseBadRequest
from django.shortcuts import render,redirect
from Memory.face_id import FaceRecognition
from django.contrib.auth import logout
from django.contrib import messages
from googletrans import Translator
from Memory.models import Signups
from datetime import datetime
from .web_scrap import *
from .models import *
from .Speech import *
from .aiml import *
from .ML import *
import re

faceRecognition = FaceRecognition()
kernel = init_kernel()
translator = Translator()
urdu_pattern = r'^[\u0600-\u06FF\s]+$'

def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('index')

def index(request):
    session = request.session.get('user_id')
    return render(request,'index.html',{'session':session})

def login(request):
    return render(request, 'login.html')   

def signup_login(request, action=None):
    face_id = None
    if request.method == "POST":
        if action == 'signup':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            dob_str = request.POST.get('dob')
            has_webcam = request.POST.get('has_webcam', )
            print(has_webcam)
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponseBadRequest("Invalid date format for date of birth.")
            else:
                return HttpResponseBadRequest("Date of birth is required.")
            gen = predict_gender(name)
            user = Signups(username=name, email=email, password=password, dob=dob, gender=gen)
            user.save()
            user_element_id = user.element_id
            if user_element_id[-2] == ":":
                face_id = user_element_id[-1:]
            else:
                face_id = user_element_id[-2:]
            user.uid = face_id
            user.save()
            print("Id===", face_id)
            if has_webcam:
                addFace(face_id)
            request.session['user_id'] = face_id or user.uid
            return redirect('index')

        else:
            if action == 'login':
                mail = request.POST.get('emailid')
                passcode = request.POST.get('password')
                user = Signups.nodes.get(email=mail, password=passcode)
                request.session['user_id'] = face_id or user.uid
                if user:
                    return redirect('index')
                else:
                    return HttpResponse('Wrong Email or Password')
                     
    return render(request, 'login.html')

def face_id(request):
    face_id = faceRecognition.recognizeFace()
    if not face_id:
        return HttpResponse('Face id Not Found try using login form')
    try:
        user = Signups.nodes.filter(uid=face_id).get()
        if user:
            request.session['user_id'] = face_id
            return redirect('index')
        else:
            return HttpResponse('No Face id Found')
    except Signups.DoesNotExist:
        return HttpResponse('User not found')

def contact(request):
    return render(request,'contact-us.html')

def signout(request):
    logout(request)
    return redirect('index')
    
def chat(request):
    session = request.session.get('user_id')
    try:
        if session:
            user = Signups.nodes.filter(uid=session).get()
        else:
            messages.error(request, 'You must log in to access the chat.')
            return redirect('index')
    except:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('index')

    if request.method == 'POST':
        message = request.POST.get('message', '')
        kernel.setPredicate('name',user.username)
        kernel.setPredicate('gender',user.gender)
        if message:
            if  re.match(urdu_pattern, message):
                english = translator.translate(message).text
                response = kernel.respond(english)
                bot_response = translator.translate(response, dest='ur').text
            else:
                bot_response = kernel.respond(message)
                if bot_response == "I'm sorry, I didn't understand what you said.":
                    bot_response = web_scraping(message)
            return JsonResponse({'bot_response': bot_response})
                
    return render(request, 'chat.html')