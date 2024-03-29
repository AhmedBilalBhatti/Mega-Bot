from django.http import JsonResponse

def prolog_handling(request):
    if request.method == 'POST' and request.FILES.get('prolog_file'):
        prolog_file = request.FILES['prolog_file']
        if prolog_file:
            print(f"Received file: {prolog_file.name}")
            return JsonResponse({'bot_response': 'This is a Prolog file I have read. What do you want to know?'})
    return JsonResponse({'bot_response': 'No file received.'})