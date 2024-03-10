from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty
from django.conf import settings
from django.db import models

class Signups(StructuredNode):
    uid = StringProperty()
    username = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    dob = DateProperty()
    face_id = StringProperty(upload_to='profile_image', blank=True)



class User_Chat(StructuredNode):
    email = StringProperty(unique_index=True)
    name = StringProperty()
    chat = ArrayProperty(StringProperty())
    created_at = DateTimeProperty(default_now=True)

    def save_message(self, message_content):
        if self.chat is None:
            self.chat = []

        self.chat.append(message_content)
        self.save()