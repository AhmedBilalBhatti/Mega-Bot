from transformers import BartTokenizer, BartForConditionalGeneration
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 


def summary(text):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
     
    # text = "Hi there"
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w in stop_words]
     
    # Prepare text for LDA
    texts = [filtered_text]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
     
    # Train LDA model with more topics and words
    lda_model = models.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=50)
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)
     
    # Tokenize input text
    inputs = tokenizer.encode(text, return_tensors='pt')
    summary_ids = model.generate(inputs, num_beams=4, max_length=20, early_stopping=True)
    final = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    final_string = " ".join(final)
    final_string2 = final_string.split('.')[0] + '.'
    return final_string2
    
 
 
 
 
from django.core.cache import cache
from django.http import JsonResponse
from celery import shared_task
 
@shared_task
def generate_summary(text):
    # Your existing code here...
    # Return the final summary instead of printing it
    return final_string.split('.')[0] + '.'
 
def summary_view(request):
    text = request.GET.get('text')
    cache_key = f'summary:{text}'
    summary = cache.get(cache_key)
    if summary is None:
        # The summary wasn't in the cache, so we need to generate it
        # This will run the task asynchronously and return immediately
        generate_summary.delay(text)
        return JsonResponse({'status': 'processing'})
    else:
        # The summary was in the cache, so we can return it immediately
        return JsonResponse({'summary': summary})