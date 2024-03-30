from django.http import JsonResponse
import pytholog as pl

def prolog_handling(request):
    if request.method == 'POST' and request.FILES.get('prolog_file'):
        prolog_file = request.FILES['prolog_file']
        if prolog_file:
            print(prolog_file)
            # prolog_contents = prolog_file.read().decode('utf-8')
            # print(prolog_contents)





            new_kb = pl.KnowledgeBase("family")
            new_kb.clear_cache()
            path = "prolog_file"
            new_kb.from_file(path)
            print(new_kb.query(pl.Expr("Parent(Ahmed,Ali)"))[0])
            print(new_kb.query(pl.Expr("Child(Alia, Nadia)"))[0])




            
            return JsonResponse({'bot_response': 'This is a Prolog file I have read. What do you want to know?'})
    
    return JsonResponse({'bot_response': 'No file received.'})






