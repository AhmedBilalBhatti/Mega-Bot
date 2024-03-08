from django.shortcuts import render,redirect
from django.conf import settings
from Memory.face_id import FaceRecognition
from django.http import HttpResponse ,JsonResponse
from .models import *
from datetime import datetime
from Memory.models import Signups
from MegaBot.settings import BASE_DIR

faceRecognition = FaceRecognition()

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


def signup_login(request, action=None):
    if request.method == "POST":
        if action == 'signup':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            dob_str = request.POST.get('dob')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            
            # Save the user object
            user = Signups(username=name, email=email, password=password, dob=dob)
            user.save()
            
            # Get the element_id instead of id
            user_element_id = user.element_id
            addFace(user_element_id)
        else:
            print('login')
            return redirect('index')
          
    return render(request, 'login.html')




def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('index')

# def login(request):
#     face_id = faceRecognition.recognizeFace()
#     print(face_id)
#     return redirect('greeting' ,str(face_id))

# def Greeting(request,face_id):
#     face_id = int(face_id)
#     context ={
#         'user' : UserProfile.objects.get(face_id = face_id)
#     }
#     return render(request,'faceDetection/greeting.html',context=context)

