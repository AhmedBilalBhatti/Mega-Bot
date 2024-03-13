from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail


def Signup_Thanks(name, email, message):
    subject = 'Thank You for Signing Up'
    email_context = {'name': name, 'email': email, 'message': message}
    html_message = render_to_string('Thanks.html', email_context)
    recipient_list = [email]
    
    try:
        send_mail(subject, '', 'ahmadbilalssg@gmail.com', recipient_list, html_message=html_message, fail_silently=True)
        return True, 'Your message has been submitted successfully.'
    except Exception as e:
        return False, f'Failed to send confirmation email: {str(e)}'
