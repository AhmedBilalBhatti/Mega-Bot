import re
from .views import *
from .models import *
import datetime
from datetime import datetime

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


def get_after_know(s):
    parts = s.split("know")
    if len(parts) > 1:
        return parts[1].strip().split()[0].rstrip('?')
    else:
        return ""

def get_last_bot_response(session_history_data):
    bot_responses = [chat_message for chat_message in session_history_data.memory_list if chat_message.split(" - ")[1].startswith("Bot:")]
    last_two_bot_responses = bot_responses[-2:]

    second_last_response = last_two_bot_responses[1] if last_two_bot_responses else None

    te = second_last_response.split(" - ")[1]
    refine = te.split(": ")[-1]
    refined = get_after_know(refine)

    return refined