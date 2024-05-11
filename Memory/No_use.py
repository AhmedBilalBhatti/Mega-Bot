
# elif is_question(message):
#     result = pre_process(message)
#     lemmatized_tokens = result[0]
#     vect_features = result[1]
#     check = lemmatized_tokens[0]
#     person = detect_persons(lemmatized_tokens)
#     che = person[0][0]
#     ps = Prolog_Members.nodes.first(full_name=che)
#     again_check = True if ps else False
#     if person and again_check:
#         Total_person = len(person)
#         if Total_person == 1:
#             name = "".join(lemmatized_tokens[1])
#             relation = "".join(lemmatized_tokens[:-1])
#             params = {
#                 "name": name,
#                 "relation": relation}
#             cypher_query = f"""
#                 MATCH (p:Prolog_Members {{full_name: $name}})
#                 MATCH (p)-[r:`{relation}`]-(other)
#                 RETURN other.full_name; """
#             results, meta = db.cypher_query(cypher_query, params)
#             formatted_names = []
#             for result in results:
#                 other_name = result[0]
#                 formatted_names.append(other_name)
#             if len(formatted_names) == 1:
#                 name_str = formatted_names[0]
#             elif len(formatted_names) == 2:
#                 name_str = f"{formatted_names[0]} and {formatted_names[1]}"
#             else:
#                 name_str = ', '.join(formatted_names[:-1]) + f", and {formatted_names[-1]}"

#             bot_response = f"{name_str.capitalize()} is {relation} of {name.capitalize()}."
#             maintain_history(request, message, bot_response)
#             return JsonResponse({'bot_response': bot_response})
    # else:
    #     bot_response = kernel.respond(message)
    #     return JsonResponse({'bot_response': bot_response})
    #     if bot_response == "I'm sorry, I didn't understand what you said.":
    #         bot_response = web_scraping(message)
    #         maintain_history(request, message, bot_response)
    #         return JsonResponse({'bot_response': bot_response})