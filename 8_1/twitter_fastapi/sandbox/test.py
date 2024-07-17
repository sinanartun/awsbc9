import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load the training dataset
df_train = pd.read_csv("twitter_financial_news_sentiment_train.csv")

# Ensure you have the necessary preprocessing functions here
def preprocess(text: str) -> str:
    import re
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    import nltk

    # Ensure the required NLTK data is downloaded
    nltk.download('stopwords')
    nltk.download('wordnet')

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

# Check column names
print(df_train.columns)

# Update to correct column names based on the dataset
# Assuming the text column is 'text' and sentiment column is 'label'
df_train['text'] = df_train['text'].apply(preprocess)

# Train the TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df_train['text'])

# Train the model
model = LogisticRegression()
model.fit(X, df_train['label'])  # Assuming 'label' is the label column

# Save the model and vectorizer
joblib.dump(model, 'logistic_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
