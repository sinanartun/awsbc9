import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

import nltk
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.sentiment import SentimentIntensityAnalyzer
from warnings import filterwarnings
import joblib



df = pd.read_csv("twitter_financial_news_sentiment_train.csv")

def preprocess(df, target):
    df[target] = df[target].str.lower()
    df[target] = df[target].str.replace('[^\w\s]', '')
    df[target] = df[target].str.replace('\d', '')
    df[target] = df[target].str.replace('\$\w+', '', regex=True)
    df[target] = df[target].str.replace('https?://\S+', '', regex=True)
    df[target] = df[target].str.replace('-', '', regex=True).str.strip()
    
    nltk.download('stopwords')
    sw = stopwords.words('english')
    df[target] = df[target].apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))
    
    sil = pd.Series(' '.join(df['ytext']).split()).value_counts()[-1000:]
    df[target] = df[target].apply(lambda x: " ".join(x for x in x.split() if x not in sil))
    
    nltk.download('wordnet')
    df[target] = df[target].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    
    return df

model = joblib.load('logistic_model.joblib')

df = preprocess (df, "ytext")

def prediction_random_from_dataset(model, data):
    random_review = pd.Series(df["ytext"].sample(1).values)
    new_comment = TfidfVectorizer().fit(data).transform(random_review)
    pred = model.predict(new_comment)
    print(f'Review:  {random_review[0]} \n Prediction: {pred}')  
    return    {"comment":random_review[0], 
               "prediction":pred}  
    
prediction_random_from_dataset(model)

