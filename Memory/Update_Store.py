from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.core.files.storage import default_storage
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

            # Define the file path within the media directory
            file_path = os.path.join('Profile', new_file_name)

            # Save the file to the media directory
            with default_storage.open(file_path, 'wb') as f:
                for chunk in profile_picture.chunks():
                    f.write(chunk)

            # Update the user's profile_image property with the correct URL format
            user.profile_image = os.path.join(settings.MEDIA_URL, file_path.replace('\\', '/'))
            user.save()

            # Redirect to the chat page after successful upload
            return redirect('chat')
        except Signups.DoesNotExist:
            return HttpResponseNotFound('User not found.')

    return HttpResponse('No file selected or invalid request.')