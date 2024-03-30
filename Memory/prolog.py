from django.http import JsonResponse
from django.conf import settings
import pytholog as pl
from .views import *
import os

def prolog_handling(request):
    session = request.session.get('user_id')
    if request.method == 'POST' and request.FILES.get('prolog_file'):
        prolog_file = request.FILES['prolog_file']
        if prolog_file:
            prolog_contents = prolog_file.read().decode('utf-8')
            print(prolog_contents)

            media_folder = settings.MEDIA_ROOT
            temp_file_path = os.path.join(media_folder, f"prolog/temp_prolog_file_{session}.pl")

            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(prolog_contents)

            new_kb = pl.KnowledgeBase("family")
            new_kb.clear_cache()
            new_kb.from_file(temp_file_path)

            parent_query_result = new_kb.query(pl.Expr("Parent(Ahmed,Ali)"))
            child_query_result = new_kb.query(pl.Expr("Child(Alia, Nadia)"))

            print(parent_query_result[0] if parent_query_result else "No result")
            print(child_query_result[0] if child_query_result else "No result")

            return JsonResponse({'bot_response': 'This is a Prolog file I have read. What do you want to know?'})

    return JsonResponse({'bot_response': 'No file received.'})
