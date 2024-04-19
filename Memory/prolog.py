from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.conf import settings
import pytholog as pl
from .models import *
from .views import *
import os
import re

names_rules = []
pure_rules = []
path = None


def extract_relation_from_fact(fact):
    # Split the fact by ':-' and get the first part
    parts = fact.split(':-')
    if len(parts) > 0:
        return parts[0].strip()  # Extract the first part and strip any extra spaces
    else:
        return None  # Return None if splitting did not yield any parts

def extract_relations_from_facts(facts):
    relations = []
    for fact in facts:
        relation = extract_relation_from_fact(fact)
        if relation:
            relations.append(relation)
    return relations






def perform_replacements(rule, name):
    rule = re.sub(r'\bX\b', name, rule)
    rule = re.sub(r'\bY\b', 'X', rule)
    return rule

def execute_prolog_query(rule):
    try:
        new_kb = pl.KnowledgeBase("family")
        new_kb.clear_cache()
        new_kb.from_file(path)
        result = new_kb.query(pl.Expr(rule))
    
        return result
    except Exception as e:
        print(f"Error executing Prolog query for rule: {rule}")
        return None

def process_names_rules(names_rules, pure_rules):
    for name in names_rules:
        print(f"Processing name: {name}")
        for rule in pure_rules:
            replaced_rule = perform_replacements(rule, name)
            print(f"Replacing placeholders in rule with name '{name}': {replaced_rule}")

            result = execute_prolog_query(replaced_rule)
            if result:
                names = [name_dict['X'] for name_dict in result if 'X' in name_dict]
                print(names)
            else:
                print(f"No result obtained for name '{name}' and rule: {replaced_rule}")







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

            path = temp_file_path

            statements = prolog_contents.splitlines()
            facts, rules = classify_statements(statements)
            pure_rules = extract_relations_from_facts(rules)
            for fact in facts:
                predicate = count_commas_in_parentheses(fact)
                att = extract_predicate(fact)
                names = extract_arguments(fact)

                if predicate == 0:
                    if names:
                        # created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        # node = Prolog_Members(uid=session, full_name=names, attribute=att, created_at=created_at)
                        # node.save()
                        names_rules.append(names)
                        print(names_rules)

                elif predicate == 1:
                    created_at_threshold = datetime.now() - timedelta(seconds=10)
                    name1, name2 = names.split(',')
                    name1 = name1.strip()
                    name2 = name2.strip()

                    # try:
                    #     existing_node1 = Prolog_Members.nodes.filter(full_name=name1, created_at__gte=str(created_at_threshold)).first()
                    # except:
                    #     existing_node1 = Prolog_Members(uid=session, full_name=name1, created_at=created_at_threshold.strftime('%Y-%m-%d %H:%M:%S'))
                    #     existing_node1.save()

                    # try:
                    #     existing_node2 = Prolog_Members.nodes.filter(full_name=name2, created_at__gte=str(created_at_threshold)).first()
                    # except:
                    #     existing_node2 = Prolog_Members(uid=session, full_name=name2, created_at=created_at_threshold.strftime('%Y-%m-%d %H:%M:%S'))
                    #     existing_node2.save()

                    # if existing_node1 and existing_node2:
                    #     existing_node1.parent.connect(existing_node2)

                elif predicate > 1:
                    nodes = []
                    for name in names:
                        nodes.append(Prolog_Members(uid=session, full_name=name).save())
                        
                        node_1 = nodes[0]
                        for node in nodes[1:]:
                            node_1.related_to.connect(node)
                            node_1 = node 
                else:
                    continue

                # print("".join(pure_rules))

                process_names_rules(names_rules, pure_rules)

            # ===================================================================


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
