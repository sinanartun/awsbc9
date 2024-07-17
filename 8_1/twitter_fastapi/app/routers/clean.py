from ..models.clean import Clean
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Ensure the required NLTK data is downloaded
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text: str) -> str:
    # Convert to lower case
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove digits
    text = re.sub(r'\d', '', text)
    
    # Remove currency symbols
    text = re.sub(r'\$\w+', '', text)
    
    # Remove hyphens and strip whitespace
    text = text.replace('-', '').strip()
    
    # Remove stop words
    text = " ".join(word for word in text.split() if word not in stop_words)
    
    # Lemmatize words
    text = " ".join(lemmatizer.lemmatize(word) for word in text.split())
    
    return text

def clean_text(clean: Clean):
    cleaned_text = preprocess(clean.text)
    return {"text": cleaned_text, "status": "cleaned"}
