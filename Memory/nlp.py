import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from string import punctuation

def preprocess_text(text):
    try:
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english') + list(punctuation))
        lemmatizer = WordNetLemmatizer()
        filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
        
        return {'tokens': tokens,'filtered_tokens': filtered_tokens,'lemmatized_tokens': filtered_tokens}
        
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None