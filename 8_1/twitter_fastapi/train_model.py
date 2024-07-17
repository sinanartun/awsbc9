import pandas as pd
from nltk.corpus import stopwords
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.sentiment import SentimentIntensityAnalyzer
import joblib
from warnings import filterwarnings

filterwarnings('ignore')

# Load the training dataset
df = pd.read_csv("twitter_financial_news_sentiment_train.csv")

# Ensure the required NLTK data is downloaded
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')  # Add this line to download the vader_lexicon

# Define the preprocessing function
def preprocess(text: str) -> str:
    import re
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

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

# Preprocess the text data
df['text'] = df['text'].apply(preprocess)

# Polarity scores
sia = SentimentIntensityAnalyzer()

# Sentiment Labels
df["Sentiment_Label"] = df["text"].apply(lambda x: 
    "bullish" if sia.polarity_scores(x)["compound"] > 0.2 else 
    "bearish" if sia.polarity_scores(x)["compound"] < -0.2 else 
    "neutral")

# Split the data
train_x, test_x, train_y, test_y = train_test_split(df["text"], df["Sentiment_Label"], random_state=42)

# TF-IDF Word Level
tf_idf_word_vectorizer = TfidfVectorizer().fit(train_x)
x_train_tf_idf_word = tf_idf_word_vectorizer.transform(train_x)
x_test_tf_idf_word = tf_idf_word_vectorizer.transform(test_x)

# Train the RandomForest model
rf_model = RandomForestClassifier().fit(x_train_tf_idf_word, train_y)

# Evaluate the model


# Save the model and vectorizer
joblib.dump(rf_model, 'app/models/logistic_model.pkl')
joblib.dump(tf_idf_word_vectorizer, 'app/models/tfidf_vectorizer.pkl')
