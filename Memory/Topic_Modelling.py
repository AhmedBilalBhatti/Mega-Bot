from transformers import BartTokenizer, BartForConditionalGeneration
from nltk.tokenize import word_tokenize
from django.http import JsonResponse
from django.core.cache import cache
from gensim import corpora, models
from nltk.corpus import stopwords
from celery import shared_task
from datetime import datetime
from .models import *
from .views import *
import datetime


tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')




def Topic_Generate(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w in stop_words]

    texts = [filtered_text]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = models.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=50)
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)

    inputs = tokenizer.encode(text, return_tensors='pt')
    summary_ids = model.generate(inputs, num_beams=4, max_length=20, early_stopping=True)
    final = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    final_string = " ".join(final)
    Topic_final = final_string.split('.')[0] + '.'
    print(Topic_final)
    return Topic_final



def format_data(request): 
    session = request.session.get('user_id')
    current_user = Signups.nodes.filter(uid = session).first()
    today = datetime.today()
    formatted_today = today.strftime('Episode - %Y-%m-%d')

    today_data = Session_History.nodes.get(name = formatted_today)

    print(today_data.memory_list)


