import aiml
import nltk 
import os
from django.conf import settings
from Neo4j.models import *


def init_kernel():
    kernel = aiml.Kernel()
    kernel.bootstrap(learnFiles=os.path.abspath("Neo4j/Data/*.aiml"))
    return kernel