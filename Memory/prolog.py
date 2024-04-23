from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship
from datetime import datetime, timedelta
from django.http import JsonResponse
from collections import defaultdict
from django.conf import settings
from neomodel import db
import pytholog as pl
from .models import *
from .views import *
import random
import os
import re

names_rules = []
pure_rules = []
path = None

responses = [
    'This is a Prolog file I have read. What do you want to know?',
    'I have processed the Prolog file. What would you like to inquire about?',
    'Please specify your query based on the Prolog file you provided.',
    'What specific information are you looking for in this Prolog file?'
]

x = "Knowledge"
new_kb = pl.KnowledgeBase(x)
new_kb.clear_cache()

def extract_relation_from_fact(fact):
    parts = fact.split(':-')
    if len(parts) > 0:
        return parts[0].strip() 
    else:
        return None  

def extract_relations_from_facts(facts):
    relations = []
    for fact in facts:
        relation = extract_relation_from_fact(fact)
        if relation:
            relations.append(relation)
    return relations

def extract_main_relation(rule):
    match = re.search(r'^\s*([\w\s]+)\s*\(.*\)', rule)
    if match:
        main_relation = match.group(1).strip()
        return main_relation
    else:
        return None

def perform_replacements(rule, name):
    rule = re.sub(r'\bX\b', name, rule)
    rule = re.sub(r'\bY\b', 'X', rule)
    return rule

def execute_prolog_query(rule):
    try:
        result = new_kb.query(pl.Expr(rule))
        return result
    except Exception as e:
        print(f"Error executing Prolog query for rule: {rule}")
        return None

def process_names_rules(names_rules, pure_rules):
    result_tuples = []
    for name in names_rules:
        for rule in pure_rules:
            replaced_rule = perform_replacements(rule, name)
            result = execute_prolog_query(replaced_rule)
            if result:
                names = [name_dict['X'] for name_dict in result if 'X' in name_dict]
                relation = extract_main_relation(rule)
                if names:
                    result_tuples.append((name, relation, names))
            else:
                print(f"No result obtained for name '{name}' and rule: {replaced_rule}")

    return result_tuples


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

            try:
                new_kb.from_file(temp_file_path)
            except SyntaxError as e:
                print(f"Syntax error in Prolog file: {e}")
                return HttpResponse("Syntax error in Prolog file.", status=400)

            statements = prolog_contents.splitlines()
            facts, rules = classify_statements(statements)
            pure_rules = extract_relations_from_facts(rules)
            for fact in facts:
                predicate = count_commas_in_parentheses(fact)
                att = extract_predicate(fact)
                names = extract_arguments(fact)

                if predicate == 0:
                    if names:
                        try:
                            node = Prolog_Members.nodes.first(uid=session, full_name=names)
                        except:
                            node = Prolog_Members(uid=session, full_name=names).save()

                        attribute = Attribute(uid=session, attribute=att).save()

                        node.fact.connect(attribute)
                        names_rules.append(names)

                elif predicate == 1:
                    created_at_threshold = datetime.now() - timedelta(seconds=10)
                    name1, name2 = names.split(',')
                    name1 = name1.strip()
                    name2 = name2.strip()
                    try:
                        check = Prolog_Members.nodes.first(full_name=name1, created_at__gte=created_at_threshold)
                    except:
                        check = Prolog_Members(uid=session, full_name=name1).save()
                    if check:
                        params = {"name1": name1,"name2": name2,"session":session,"att": att}
                        if params:
                            cypher_query = f"""
                                MATCH (n1:Prolog_Members {{uid: $session, full_name: $name1}})
                                MATCH (n2:Prolog_Members {{uid: $session, full_name: $name2}})
                                CREATE (n1)-[r:`{att}`]->(n2)
                                RETURN r
                            """
                            results, meta = db.cypher_query(cypher_query, params)
                            print(results,meta)

                elif predicate > 1:
                    created_at_threshold = datetime.now() - timedelta(seconds=10)
                    nodes = []
                    for name in names:
                        part1, part2, *z_values = name.split(',')
                        x_name = part1.strip()
                        y_name = part2.strip()
                        z_values = [z.strip() for z in z_values]
                        try:
                            x_node = Prolog_Members.nodes.first(full_name=x_name, created_at__gte=str(created_at_threshold))
                        except:
                            x_node = Prolog_Members(uid=session, full_name=x_name, created_at=created_at_threshold.strftime('%Y-%m-%d %H:%M:%S')).save()
                        try:
                            x_node = Prolog_Members.nodes.first(full_name=y_name, created_at__gte=str(created_at_threshold))
                        except:
                            y_node = Prolog_Members(uid=session, full_name=y_name, created_at=created_at_threshold.strftime('%Y-%m-%d %H:%M:%S')).save()

                        if x_node and y_node:
                            params = {
                                    "x_name": x_name,
                                    "y_name": y_name,
                                    "att": att
                                }
                            cypher_query = f"""
                                MATCH (n1:Prolog_Members {{full_name: $x_name}})
                                MATCH (n2:Prolog_Members {{full_name: $y_name}})
                                CREATE (n1)-[r:`{att}`]->(n2)
                                RETURN r
                            """
                            results, meta = db.cypher_query(cypher_query, params)

                        for z_value in z_values:
                            z_attribute_node = Attribute(uid=session, attribute=z_value).save()

                            if y_node and z_attribute_node:
                                params = {
                                    "y_name": y_name,
                                    "z_value": z_value
                                }
                                cypher_query = """
                                    MATCH (n2:Prolog_Members {full_name: $y_name})
                                    MATCH (z:Attribute {attribute: $z_value})
                                    CREATE (n2)-[r:HAS]->(z)
                                    RETURN r
                                """
                                results, meta = db.cypher_query(cypher_query, params)
                else:
                    continue

            created_at_threshold = datetime.now() - timedelta(seconds=10)
            result_tuples = process_names_rules(names_rules, pure_rules)

            if result_tuples:
                for name11, relation12, name22_list in result_tuples:
                    print(f"- {name11} -> is {relation12} of -> {name22_list}")

                    for name22 in name22_list:
                        name22 = name22.strip()

                    params = {
                        "name11": name11,
                        "name22": name22,
                        "session": session,
                        "relation12": relation12
                    }

                    cypher_query_check = f"""
                        MATCH (n1:Prolog_Members {{uid: $session, full_name: $name11}})-[r:`{relation12}`]->(n2:Prolog_Members {{uid: $session, full_name: $name22}})
                        RETURN r
                    """
                    existing_relationships, _ = db.cypher_query(cypher_query_check, params)

                    if not existing_relationships and name11 != name22:
                        cypher_query_create = f"""
                            MATCH (n1:Prolog_Members {{uid: $session, full_name: $name11}})
                            MATCH (n2:Prolog_Members {{uid: $session, full_name: $name22}})
                            CREATE (n1)-[r:`{relation12}`]->(n2)
                            RETURN r
                        """
                        try:
                            results, meta = db.cypher_query(cypher_query_create, params)
                            print(results)
                        except Exception as e:
                            print(f"Error executing Cypher query: {e}")

            return JsonResponse({'bot_response': random.choice(responses)})
    return JsonResponse({'bot_response': 'No file received.'})


# ====================================================================================================================================

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
