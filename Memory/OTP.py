from django.http import HttpResponse ,JsonResponse,HttpResponseBadRequest
from .views import *



def forgot1(request):
    if request.method == 'POST':
        try:
            email_user = request.POST.get('email')
            if not email_user:
                return JsonResponse({'message': 'Email is required'}, status=400)

            otppassword = generate_random_otp()
            useremail = "ahmadbilalssg@gmail.com"  
            set_session(request, "userOTP", otppassword)
            set_session(request, "email", email_user)
            send_email(request, otppassword, useremail)

            return redirect('otpverifcation')
        except Exception as e:
            return JsonResponse({'status': 'An unexpected error occurred'}, status=500)

    return render(request, 'Staff/forgot-password.html')

@requires_forgot1
def otpverifcation(request):
    if request.method == 'POST':
        optCode0=request.POST['otp_input']
        optCode1=request.POST['otp_input1']
        optCode2=request.POST['otp_input2']
        optCode3=request.POST['otp_input3']
        optCode = optCode0+optCode1+optCode2+optCode3
        try:
            otpUser =  get_session_with_expiry(request , 'userOTP')
            email =  get_session_with_expiry(request , 'email')
            if otpUser is None: 
                return HttpResponse('The Otp expired')
            else:
                if int(optCode) == int(otpUser):
                    return redirect('forgot3')
                else: 
                    return HttpResponse('Wrong OTP')
        except Exception as e:
            print("3 pass 3")

    return render(request, 'Staff/otp.html')

@requires_otp_verification
def forgot3(request):
    if request.method == 'POST':
        new_p = request.POST['new_password']
        email = get_session_with_expiry(request, 'email')

        if email and new_p is not None:
            try:
                r = Register_Staff.objects.get(email=email)
                if r:
                    r.password = new_p
                    r.save()
                    return redirect('login')
            except:
                try:
                    r = Admin_register.objects.get(email=email)
                    if r:
                        r.password = new_p
                        r.save()
                        return redirect('admin-login')
                except Admin_register.DoesNotExist:
                    return HttpResponse('There was a error while processing your request')
        else:
            return HttpResponse('There was a error while processing your request')

    return render(request, 'Staff/New password.html')