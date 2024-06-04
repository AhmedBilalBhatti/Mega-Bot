from .views import *
from .models import *





def search_ip(email):
    temp = ''
    response = ''
    try:
        main_user = Signups.nodes.get(email=email)
        first_ip = main_user.ip
        search = Signups.nodes.exclude(email=email)
        for user in search:
            if user.ip == first_ip:
                temp = user.username
                response = f'Do you know {temp}?'
                break
        return response

    except Signups.DoesNotExist:
        return False

