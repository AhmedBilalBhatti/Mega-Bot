from django.core.files.storage import default_storage
from django.urls import reverse
from django.http import HttpResponseNotFound
from .models import *
import os


def upload_profile_pic(request):
    session = request.session.get('user_id')
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']

        try:
            user = Signups.nodes.get(uid=session)
            file_extension = os.path.splitext(profile_picture.name)[1]
            new_file_name = f"profile_{session}{file_extension}"

            if user.profile_image:
                try:
                    default_storage.delete(user.profile_image)
                except FileNotFoundError:
                    pass

            file_path = os.path.join(settings.MEDIA_ROOT, 'Profile', new_file_name)
            with open(file_path, 'wb') as f:
                for chunk in profile_picture.chunks():
                    f.write(chunk)

            user.profile_image = os.path.join(settings.MEDIA_URL, 'Profile', new_file_name)
            user.save()

            return redirect('chat')
        except Signups.DoesNotExist:
            return HttpResponseNotFound('User not found.')

    return HttpResponse('No file selected or invalid request.')
