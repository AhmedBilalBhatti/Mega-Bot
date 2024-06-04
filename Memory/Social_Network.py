from .views import *
from .models import *





def search_ip(email):
    try:
        main_user = Signups.nodes.get(email=email)
        first_ip = main_user.ip
        search = Signups.nodes.filter(ip=first_ip).exclude(email=email)
        
        for user in search:
            temp = user.email
            response = f'Do you know {temp}?'
            return response

        return False

    except Signups.DoesNotExist:
        return False

