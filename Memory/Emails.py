from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime


def Signup_Thanks(name, email, message):
    subject = 'Thank You for Signing Up'
    email_context = {'name': name, 'email': email, 'message': message}
    html_message = render_to_string('Thanks.html', email_context)
    recipient_list = [email]
    print(email_context)
    try:
        send_mail(subject, '', 'ahmadbilalssg@gmail.com', recipient_list, html_message=html_message, fail_silently=True)
        return True, 'Your message has been submitted successfully.'
    except Exception as e:
        return False, f'Failed to send confirmation email: {str(e)}'


def Login_Trigger(name, email):
    subject = 'Login Notification'
    login_datetime = timezone.now()
    login_datetime_local = timezone.localtime(login_datetime)
    login_date = login_datetime_local.strftime('%Y-%m-%d')
    login_time = login_datetime_local.strftime('%H:%M:%S')
    email_context = {'name': name, 'date': login_date, 'time': login_time}
    html_message = render_to_string('login_notification.html', email_context)
    recipient_list = [email]
    try:
        send_mail(subject, '', 'ahmadbilalssg@gmail.com', recipient_list, html_message=html_message, fail_silently=True)
        return True, 'Login notification sent successfully.'
    except Exception as e:
        return False, f'Failed to send login notification email: {str(e)}'
