from django.http import HttpResponse
from django.conf import settings
import os
import speech_recognition as sr

# def speech_to_text(request):
#     if request.method == 'POST':
#         r = sr.Recognizer()
#         audio_data = request.FILES['audio'].read()
#         audio_path = os.path.join(settings.BASE_DIR, 'Audio', 'audio.wav')
#         with open(audio_path, 'wb') as f:
#             f.write(audio_data)
    
#         with sr.AudioFile(audio_path) as source:
#             audio_data = r.record(source)
#             text = r.recognize_google(audio_data, language='en-IN', show_all=True)
#             print(text)
#             return_text = "Did you say:<br>"
#             try:
#                 for num, texts in enumerate(text['alternative']):
#                     return_text += str(num + 1) + ") " + texts['transcript'] + "<br>"
#             except:
#                 return_text = "Sorry!!!! Voice not Detected"

#         # return HttpResponse(return_text)
#         return return_text


def speech_to_text(request):
    if request.method == 'POST':
        r = sr.Recognizer()
        audio_data = request.FILES['audio'].read()
        audio_path = os.path.join(settings.BASE_DIR, 'Audio', 'audio.wav')
        with open(audio_path, 'wb') as f:
            f.write(audio_data)

        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='en-IN', show_all=True)
            print(text)
            return_text = ""
            try:
                for num, texts in enumerate(text['alternative']):
                    return_text += str(num + 1) + ") " + texts['transcript'] + "\n"
            except:
                return_text = "Sorry!!!! Voice not Detected"

        return return_text

