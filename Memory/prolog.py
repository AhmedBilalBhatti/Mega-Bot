from django.http import JsonResponse
from django.conf import settings
import pytholog as pl
from .models import *
from .views import *
import os


def read_prolog_file(file):
    statements = []
    
    for line in file:
        line = line.strip()
        if line and not line.startswith('%'):
            statements.append(line)
    
    return statements

def classify_statements(statements):
    facts = []
    rules = []
    
    for statement in statements:
        statement = statement.strip()
        
        if statement.endswith('.'):
            statement = statement[:-1].strip()
        
        if statement and ':-' in statement:
            rules.append(statement)
        elif statement:
            facts.append(statement)
    
    return facts, rules

def prolog_handling(request):
    session = request.session.get('user_id')
    
    if request.method == 'POST' and request.FILES.get('prolog_file'):
        prolog_file = request.FILES['prolog_file']
        
        if prolog_file:
            prolog_contents = prolog_file.read().decode('utf-8')
            print(prolog_contents)

            media_folder = settings.MEDIA_ROOT
            temp_file_path = os.path.join(media_folder, f"prolog/temp_prolog_file_{session}.pl")

            if default_storage.exists(temp_file_path):
                default_storage.delete(temp_file_path)

            with default_storage.open(temp_file_path, 'w') as temp_file:
                temp_file.write(prolog_contents)

            new_kb = pl.KnowledgeBase("custom_kb")
            new_kb.clear_cache()
            
            # Read and process Prolog statements from the uploaded file
            with open(temp_file_path, 'r') as prolog_file:
                prolog_statements = read_prolog_file(prolog_file)
            
            # Classify Prolog statements into facts and rules
            facts, rules = classify_statements(prolog_statements)
            
            # Load classified statements into the KnowledgeBase
            for fact in facts:
                new_kb(fact)  # Assert each fact into the KnowledgeBase
            
            for rule in rules:
                new_kb(rule)  # Assert each rule into the KnowledgeBase

            return JsonResponse({'bot_response': 'Prolog file processed successfully.'})

    return JsonResponse({'bot_response': 'No file received.'})





def make_graph(session, node1, node1_gender, relationship_type, node2, node2_gender):
    node_1 = Prolog_Members(uid=session, name=node1, gender=node1_gender)
    node_1.save()

    node_2 = Prolog_Members(uid=session, name=node2, gender=node2_gender)
    node_2.save()

    node_1.add_relationship(node_2, relationship_type)


