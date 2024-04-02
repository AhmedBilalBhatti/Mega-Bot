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
            print(prolog_contents)

            media_folder = settings.MEDIA_ROOT
            temp_file_path = os.path.join(media_folder, f"prolog/temp_prolog_file_{session}.pl")

            # Remove the previous file if it exists
            if default_storage.exists(temp_file_path):
                default_storage.delete(temp_file_path)

            # Save the uploaded file
            with default_storage.open(temp_file_path, 'w') as temp_file:
                temp_file.write(prolog_contents)

            new_kb = pl.KnowledgeBase("family")
            new_kb.clear_cache()
            new_kb.from_file(temp_file_path)

            true_facts = extract_facts(prolog_contents)

            print('\n')
            print('\n')
            print(true_facts)
            print('\n')
            print('\n')
            result = extract_prolog_info(true_facts)
            print(result)
            return JsonResponse({'bot_response': 'This is a Prolog file I have read. What do you want to know?'})

    return JsonResponse({'bot_response': 'No file received.'})


def extract_facts(prolog_contents):
    facts = []
    lines = prolog_contents.split('\n')
    for line in lines:
        line = line.strip()
        if line and line[0].isalpha(): 
            parts = line.split('(')
            predicate = parts[0]
            person = parts[1].split(',')[0]
            facts.append((predicate, person))
    return facts



def extract_prolog_info(true_facts):
    prolog_info = []
    for fact in true_facts:
        relationship, individuals = fact
        individual_names = []

        # Check if individuals is a string or a tuple
        if isinstance(individuals, str):
            # Extract individual name from the string
            individual_name = individuals.rstrip(').').split()[-1]
            individual_names.append(individual_name)
        elif isinstance(individuals, tuple):
            # Extract individual names from the tuple
            for individual in individuals:
                individual_name = individual.rstrip(').').split()[-1]
                individual_names.append(individual_name)

        # Append the other individual names if they exist
        other_individual_names = [name for name in individual_names if name != individual_name]

        # Format the relationship and individual names into a string
        formatted_fact = f"{relationship}:{','.join(individual_names)}"

        # If other individual names exist, append them to the formatted fact
        if other_individual_names:
            formatted_fact += f",Other:{','.join(other_individual_names)}"

        # Append the formatted fact to the prolog_info list
        prolog_info.append(formatted_fact)

    return prolog_info

def make_graph(session, node1, node1_gender, relationship_type, node2, node2_gender):
    node_1 = Prolog_Members(uid=session, name=node1, gender=node1_gender)
    node_1.save()

    node_2 = Prolog_Members(uid=session, name=node2, gender=node2_gender)
    node_2.save()

    node_1.add_relationship(node_2, relationship_type)


