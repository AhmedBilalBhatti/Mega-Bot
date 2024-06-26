from neomodel import StructuredNode, StringProperty,BooleanProperty,IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty, StructuredRel
from django.conf import settings
from datetime import datetime
from django.db import models
from uuid import uuid4

class Signups(StructuredNode):
    uid = StringProperty()
    username = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    dob = DateProperty()
    gender = StringProperty(required=True)
    face_id = BooleanProperty(default=False)
    profile_image = StringProperty()
    ip = StringProperty(default=None,blank=True)

    chat = RelationshipTo('History_Chat', 'HAS')


    class Meta:
        labels = ["Signups","Person"]





class History_Chat(StructuredNode):
    uid = StringProperty()
    name = StringProperty()
    chat = ArrayProperty(StringProperty())
    created_at = DateTimeProperty(default_now=True)
    memory_list = ArrayProperty(StringProperty())

    history = RelationshipTo('Session_History', 'HAS')

class Episode_Part(StructuredNode):
    uid = StringProperty()
    name = StringProperty()
    response = StringProperty()
    sentiments = StringProperty(default=None,blank=True)
    created_at = StringProperty(default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    relation = RelationshipFrom('Session_History', 'HAS_CHAT')





class Session_History(StructuredNode):
    uid = StringProperty()
    name = StringProperty()
    start_session = DateTimeProperty(default_now=True)
    sentiments = StringProperty(default=None,blank=True)
    memory_list = ArrayProperty(StringProperty())

    def save_message(self, message_type, message_content):
        if self.memory_list is None:
            self.memory_list = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} - {message_type}: {message_content}"
        self.memory_list.append(formatted_message)
        self.save()

class Person(StructuredNode):
    uid = StringProperty(blank=True)
    full_name = StringProperty(blank=True)
    created_at = StringProperty(default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    parent = RelationshipTo('Person','IS_PARENT_OF')
    fact  = RelationshipTo('Attribute','IS')

class Attribute(StructuredNode):
    uid = StringProperty(blank=True)
    attribute = StringProperty(blank=True)
    created_at = StringProperty(default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class SocialNetwork(StructuredNode):
    uid = StringProperty(unique_index=True)
    name = StringProperty()
    gender = StringProperty()
    created_at = StringProperty(default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = str(uuid4())


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