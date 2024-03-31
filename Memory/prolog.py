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






            facts = extract_facts(prolog_contents)
            true_facts = []

            # Test each possible query and collect true facts with person
            for predicate, person in facts:
                result = new_kb.query(pl.Expr(predicate))
                if result:
                    true_facts.append((predicate, person))

            # Extract relationships from the true facts
            relationships = []
            for fact in true_facts:
                predicate, person = fact
                # Check if the predicate implies a relationship
                if 'Parent' in predicate:
                    # Ensure the predicate contains '(' before splitting
                    if '(' in predicate:
                        try:
                            subject, object_ = predicate.split('(')[1].split(',')
                            relationships.append(f"{subject.strip()} is a {predicate.split('(')[0].strip()} of {object_.strip()}")
                        except IndexError:
                            # Handle the case where splitting fails
                            print(f"Failed to extract relationship from predicate: {predicate}")
                    else:
                        # Handle cases where '(' is not found in the predicate
                        print(f"Predicate does not contain '(': {predicate}")

            print(true_facts)
            print(relationships)
            # print(parent_query_result = new_kb.query(pl.Expr("Parent(Ahmed,Ali)")))
            # print(child_query_result = new_kb.query(pl.Expr("Child(Alia, Nadia)")))


            return JsonResponse({'bot_response': 'This is a Prolog file I have read. What do you want to know?'})

    return JsonResponse({'bot_response': 'No file received.'})


def extract_facts(prolog_contents):
    # Extract facts with person from prolog contents
    # Assuming each fact is on a separate line and has a single predicate
    facts = []
    lines = prolog_contents.split('\n')
    for line in lines:
        line = line.strip()
        if line and line[0].isalpha():  # Assuming predicates start with alphabetic characters
            parts = line.split('(')
            predicate = parts[0]
            person = parts[1].split(',')[0].strip()[:-1]  # Extract the person without the closing parenthesis
            facts.append((predicate, person))
    return facts




def make_graph():
    pass