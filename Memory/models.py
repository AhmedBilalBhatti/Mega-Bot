from neomodel import StructuredNode, StringProperty,BooleanProperty,IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty
from django.conf import settings
from datetime import datetime
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

    chat = RelationshipTo('History_Chat', 'HAS')


    class Meta:
        labels = ["Signups","Person"]

class History_Chat(StructuredNode):
    uid = StringProperty()
    name = StringProperty()
    chat = ArrayProperty(StringProperty())
    created_at = DateTimeProperty(default_now=True)
    # sentiments = StringProperty()
    memory_list = ArrayProperty(StringProperty())

    history = RelationshipTo('Session_History', 'HAS')

class Session_History(StructuredNode):
    uid = StringProperty()
    name = StringProperty()
    start_session = DateTimeProperty(default_now=True)
    memory_list = ArrayProperty(StringProperty())

    def save_message(self, message_type, message_content):
        if self.memory_list is None:
            self.memory_list = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} - {message_type}: {message_content}"
        self.memory_list.append(formatted_message)
        self.save()




class Prolog_Members(StructuredNode):
    uid = StringProperty(blank=True)
    full_name = StringProperty(blank=True)  # Store the full name as a single entity
    attribute = StringProperty(blank=True)
    created_at = StringProperty()  # Store datetime as string

    def add_relationship(self, other_node, relationship_type):
        relationship = RelationshipTo(self, relationship_type, other_node)
        relationship.save()

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