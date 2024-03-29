from django.http import HttpResponse ,JsonResponse,HttpResponseBadRequest


def prolog_handling(request):
    if request.method == 'POST' and request.FILES.get('prolog_file'):
        prolog_file = request.FILES['prolog_file']
        if prolog_file:
            print(f"Received filesssssssssssss: {prolog_file.name}")
            # request.session['file_received'] = True
            # bot_response = "This is a prolog file I have read. What do you want to know?"
            # return JsonResponse({'bot_response': bot_response})

    return JsonResponse({'bot_response': 'No file received.'})