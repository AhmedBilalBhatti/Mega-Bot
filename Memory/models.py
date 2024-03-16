from neomodel import StructuredNode, StringProperty,BooleanProperty,IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty
from django.conf import settings
from django.db import models

class Signups(StructuredNode):
    uid = StringProperty()
    username = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    dob = DateProperty()
    gender = StringProperty(required=True)
    face_id = BooleanProperty(default=False)
    profile_image = StringProperty()

    chat = RelationshipTo('User_Chat', 'HAS_CHAT')

class User_Chat(StructuredNode):
    user_id = IntegerProperty(unique_index=True)
    name = StringProperty()
    chat = ArrayProperty(StringProperty())
    created_at = DateTimeProperty(default_now=True)

    def save_message(self, message_content):
        if self.chat is None:
            self.chat = []

        self.chat.append(message_content)
        self.save()

# =================================================================================================

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.email


class FAQS(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "FAQ"

    def __str__(self):
        return self.question