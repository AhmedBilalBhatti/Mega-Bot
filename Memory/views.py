from django.http import HttpResponse ,JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render,redirect
from Memory.face_id import FaceRecognition
from django.contrib.auth import logout
from datetime import datetime, date
from django.contrib import messages
from googletrans import Translator
from Sensory_Memory.views import *
from .Social_Network import *
from .Update_Store import *
from Memory.models import *
from .decorators import *
from .web_scrap import *
from neomodel import db
from neomodel import *
from .prolog import *
from .Emails import *
from .models import *
from .Speech import *
from .aiml import *
from .nlp import *
from .OTP import *
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
    faq = FAQS.objects.all()
    return render(request,'index.html',{'session':session,'faq':faq})

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
            has_webcam = request.POST.get('has_webcam',)
            ip_address = request.POST.get('ip_address')
            print(ip_address)
            print(has_webcam)
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    return HttpResponseBadRequest("Invalid date format for date of birth.")
            else:
                return HttpResponseBadRequest("Date of birth is required.")
            gen = predict_gender(name)
            user = Signups(username=name, email=email, password=password, dob=dob, gender=gen,ip=ip_address)
            user.save()
            msg = "We are delighted to welcome you to our community! Your registration is confirmed, and we are excited to have you on board."
            user_element_id = user.element_id
            split_element_id = user_element_id.split(":")
            face_id = split_element_id[-1]
            user.uid = face_id
            user.face_id = True
            user.save()
            Signup_Thanks(name,email,msg)
            print("Id===", face_id)
            if has_webcam:
                addFace(face_id)
            request.session['user_id'] = face_id or user.uid
            return redirect('index')
        else:
            if action == 'login':
                mail = request.POST.get('emailid')
                passcode = request.POST.get('password')
                ip_address = request.POST.get('ip_address')
                print(ip_address)
                user = Signups.nodes.get(email=mail, password=passcode)
                request.session['user_id'] = face_id or user.uid
                Login_Trigger(user.username,mail)
                if user:
                    user.ip = ip_address
                    user.save()
                    return redirect('index')
                else:
                    return HttpResponse('Wrong Email or Password')
                     
    return render(request, 'login.html')

def face_id(request):
    face_id = faceRecognition.recognizeFace()
    face_id_auth = faceRecognition.recognizeFace()
    print('id',face_id)
    print('auth',face_id_auth)
    if face_id is None and face_id_auth is None and face_id is not face_id_auth:
        return HttpResponse('Face id Not Found try using login form')
    try:
        user = Signups.nodes.filter(uid=face_id).get()
        if user:
            request.session['user_id'] = face_id or face_id_auth
            Login_Trigger(user.username,user.email)
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

def about(request):
    session = request.session.get('user_id')
    return render(request,'service.html',{'session':session})


def contact(request):
    session = request.session.get('user_id')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message = request.POST['message']
        try:
            if session:
                contact = Contact(name=name, email=email, phone_number=phone_number, message=message)
                contact.save()
                messages.success(request, 'Your message has been submitted successfully!')
                send_success_contact(request,email,name,message)
                return redirect('index')
            else:
                return redirect('login')
        except Exception as e:
            return HttpResponse('An error occurred while processing your request.')

    return render(request,'contact-us.html',{'session':session})

# =======================================================================================================
def maintain_history(request, user, bot):
    user_id = request.session.get('user_id')
    user_node = Signups.nodes.filter(uid=user_id).first()
    
    try:
        history_chat_node = History_Chat.nodes.filter(uid=user_id).first()
    except:
        history_chat_node = History_Chat(uid=user_id, name="History").save()
        user_node.chat.connect(history_chat_node)

    session_history_node = None
    
    if history_chat_node:
        start_session = datetime.combine(date.today(), datetime.min.time())
        try:
            name = f"Episode - {start_session.strftime('%Y-%m-%d')}" 
            session_history_node = Session_History.nodes.filter(uid=user_id, name=name).first()
        except:
            name = f"Episode - {start_session.strftime('%Y-%m-%d')}" 
            session_history_node = Session_History(uid=user_id, name=name).save()
            history_chat_node.history.connect(session_history_node)

    if session_history_node:
        session_history_node.save_message("User", user)
        session_history_node.save_message("Bot", bot)

def extend_episode(request,user,bot,session):
    today = datetime.combine(date.today(), datetime.min.time())
    check = f"Episode - {today.strftime('%Y-%m-%d')}"
    obj_ep = History_Chat.nodes.get(name = check,uid = session)

    user_obj = Episode_Part(uid = session,name='Bot',response=bot)
    bot_bot = Episode_Part(uid = session,name='User',response=user)


# ========================================================================================================

def chat(request):    
    session = request.session.get('user_id')
    try:
        current_user = Signups.nodes.filter(uid = session).first()
    except:
        return redirect('login')
    Session_History.nodes.filter(uid = session)
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
            bot_response = kernel.respond(message)
            if  re.match(urdu_pattern, message):
                english = translator.translate(message).text
                response = kernel.respond(english)
                bot_response = translator.translate(response, dest='ur').text
            else:
                bot_response = kernel.respond(message)

            if kernel.getPredicate("namex") and kernel.getPredicate("relationx"):
                print(kernel.getPredicate("namex"),kernel.getPredicate("relationx"))
                name = kernel.getPredicate("namex").lower()
                relation = kernel.getPredicate("relationx").lower()

                params = {"name": name,"relation": relation}
                cypher_query = f"""
                    MATCH (p:Person {{full_name: $name}})
                    MATCH (p)<-[r:`{relation}`]-(other)
                    RETURN other.full_name; """
                results, meta = db.cypher_query(cypher_query, params)

                if results:
                    formatted_names = []
                    for result in results:
                        other_name = result[0]
                        formatted_names.append(other_name)
                    if len(formatted_names) == 1:
                        name_str = formatted_names[0]
                    elif len(formatted_names) == 2:
                        name_str = f"{formatted_names[0]} and {formatted_names[1]}"
                    else:
                        name_str = ', '.join(formatted_names[:-1]) + f", and {formatted_names[-1]}"

                    if name_str != '':
                        kernel.setPredicate('namey',name_str.capitalize())
                        bot_response = kernel.respond(message)
                else:
                    bot_response = 'No knowledge Found in knowledgebase according to your Query.'

            elif kernel.getPredicate("person_sn") and kernel.getPredicate("relation_sn"):
                person_sn = kernel.getPredicate("person_sn")
                relation_sn = kernel.getPredicate("relation_sn")
                gender = predict_gender(person_sn)

                today_date = datetime.now().strftime('%Y-%m-%d')
                chk_date = f"Episode - {today_date}"
                session_history_data = Session_History.nodes.get(name=chk_date,uid=session)

                last_two_bot_responses = get_last_bot_response(session_history_data)
                name = get_last_bot_response(session_history_data)
                top = Signups.nodes.get(uid=session)
                email1 = top.email

                gen = predict_gender(name)

                params = {"name": name,"relation_sn": relation_sn,"email1":email1,"session":session}

                print(params)
                if params:
                    print('Access')
                    cypher_query = f"""
                        MATCH (p:Signups {{email:$email1}})
                        CREATE (s:SocialNetwork {{name:$name,uid:$session}})
                        CREATE (p)<-[r:`is_{relation_sn}`]-(s)
                        RETURN r; """ 
                    results, meta = db.cypher_query(cypher_query, params)

                    print(results,meta)

            elif kernel.getPredicate("takeoff"):
                Tello_Takeoff()
                return JsonResponse({'bot_response': bot_response})
        
            elif kernel.getPredicate("land"):
                Tello_Land()
            
            elif kernel.getPredicate("moveforward"):
                value = kernel.getPredicate("moveforward")
                Move_Forward(value)

            elif kernel.getPredicate("movebackward"):
                value = kernel.getPredicate("movebackward")
                Move_Backward(value)

            elif kernel.getPredicate("moveleft"):
                value = kernel.getPredicate("moveleft")
                Move_Left(value)

            elif kernel.getPredicate("moveright"):
                value = kernel.getPredicate("moveright")
                Move_Right(value)

            elif kernel.getPredicate("takepicture"):
                take_picture()

            default_message = "I'm sorry, I didn't understand what you said."
            if bot_response == default_message or default_message in bot_response or bot_response.endswith("I didn't understand what you said.") or bot_response=='':
                chk = search_ip(request,current_user.email)
                print('shkcgsdg',chk)
                if chk:
                    print('hgjkHJ')
                    bot_response = chk
                else:
                    bot_response = web_scraping(message)
            maintain_history(request, message, bot_response)
            if bot_response:
                extend_episode(request,message,bot_response,session)
            return JsonResponse({'bot_response': bot_response})

    return render(request, 'chat.html',{'current_user':current_user})





# from .Topic_Modelling import *

# format_data(request)