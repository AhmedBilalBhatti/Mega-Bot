from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty
from django.conf import settings
from django.db import models

class Signups(StructuredNode):
    username = StringProperty()
