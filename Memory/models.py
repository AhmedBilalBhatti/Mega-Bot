from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty
from django.conf import settings
from django.db import models

class Signups(StructuredNode):
    username = StringProperty(required=True)
    email = StringProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    dob = DateProperty()
    face_id = StringProperty(upload_to='profile_image', blank=True)