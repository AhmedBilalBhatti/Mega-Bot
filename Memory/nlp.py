import re
import nltk
import spacy
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text): # Special char
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


def detect_persons(text_list):
    persons = []
    for text in text_list:
        doc = nlp(text)
        entities = [(entity.text, entity.label_) for entity in doc.ents if entity.label_ == "PERSON"]
        for person, label in entities:
            persons.append(person)
    return list(set(persons))


def pre_process(text):
    vectorizer = CountVectorizer()
    preprocessed_text = preprocess_text(text)
    tokens = word_tokenize(preprocessed_text)

    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    vectorizer.fit_transform(lemmatized_tokens)
    print("Processed Text:",lemmatized_tokens)
    print("Extracted Features:", vectorizer.get_feature_names_out())
    vect_features = vectorizer.get_feature_names_out()
    return lemmatized_tokens , vect_features


def words_frequency(lemmatized_tokens):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([' '.join(lemmatized_tokens)])
    X_dense = X.toarray()
    feature_names = vectorizer.get_feature_names_out()
    total_word_frequencies = X_dense.sum(axis=0)
    word_frequencies = dict(zip(feature_names, total_word_frequencies))

    print("Word Frequencies:")
    for word, frequency in word_frequencies.items():
        print(f"{word}: {frequency}")
        return word , frequency


def is_question(text):
    question_words = ['who', 'what', 'where', 'when', 'why', 'how', 'is', 'are', 'do', 'does', 'can', 'could', 'should']
    return any(word + ' ' in text.lower() for word in question_words) or text.endswith('?')