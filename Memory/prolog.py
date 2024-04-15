from django.http import JsonResponse
from django.conf import settings
import pytholog as pl
from .models import *
from .views import *
import os

true_facts = []

def prolog_handling(request):
    session = request.session.get('user_id')
    if request.method == 'POST' and request.FILES.get('prolog_file'):
        prolog_file = request.FILES['prolog_file']
        if prolog_file:
            prolog_contents = prolog_file.read().decode('utf-8')

            media_folder = settings.MEDIA_ROOT
            temp_file_path = os.path.join(media_folder, f"prolog/temp_prolog_file_{session}.pl")

            if default_storage.exists(temp_file_path):
                default_storage.delete(temp_file_path)

            with default_storage.open(temp_file_path, 'w') as temp_file:
                temp_file.write(prolog_contents)
                print('as',temp_file)

            statements = prolog_contents.splitlines()
            facts, rules = classify_statements(statements)

            print("Facts:")
            for fact in facts:
                print(fact)

            print("\nRules:")
            for rule in rules:
                print(rule)


            for fact in facts:
                predicate = count_commas_in_parentheses(fact)
                att = extract_predicate(fact)
                names = extract_arguments(fact)

                if predicate == 0:
                    if len(names) > 0:
                        Prolog_Members(uid=session, attribute=att, name=names[0]).save()
                elif predicate == 1:
                    if len(names) > 1:
                        node_1 = Prolog_Members(uid=session, name=names[0]).save()
                        node_2 = Prolog_Members(uid=session, name=names[1]).save()
                        node_1.add_relationship(node_2)  # Connect node_1 to node_2
                elif predicate > 1:
                    nodes = [Prolog_Members(uid=session, name=name).save() for name in names]
                    for i in range(len(nodes) - 1):
                        nodes[i].add_relationship(nodes[i + 1])

            new_kb = pl.KnowledgeBase("family")
            new_kb.clear_cache()
            new_kb.from_file(temp_file_path)


            return JsonResponse({'bot_response': 'This is a Prolog file I have read. What do you want to know?'})

    return JsonResponse({'bot_response': 'No file received.'})



def read_prolog_file(file_path):
    statements = []

    with open(file_path, 'r') as file:
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

def extract_predicate(prolog_fact): # male ,femla etc
    prolog_fact = prolog_fact.strip()
    if '(' in prolog_fact:
        predicate = prolog_fact.split('(')[0]
        return predicate
    else:
        return None

def count_commas_in_parentheses(prolog_fact):
    start_index = prolog_fact.find('(')
    end_index = prolog_fact.rfind(')')
    
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        return 0
    arguments_string = prolog_fact[start_index + 1 : end_index]  
    if not arguments_string.strip():
        return 0
    
    comma_count = arguments_string.count(',')
    return comma_count

def extract_arguments(prolog_fact):
    start_index = prolog_fact.find('(')
    end_index = prolog_fact.rfind(')')
    
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        return [] 
    arguments_string = prolog_fact[start_index + 1 : end_index].strip()
    
    if not arguments_string: 
        return []
    
    names = [name.strip() for name in arguments_string.split(',')]
    return ", ".join(names)

def make_graph(session, node1, node1_gender, relationship_type, node2, node2_gender):
    node_1 = Prolog_Members(uid=session, name=node1, gender=node1_gender)
    node_1.save()

    node_2 = Prolog_Members(uid=session, name=node2, gender=node2_gender)
    node_2.save()

    node_1.add_relationship(node_2, relationship_type)
