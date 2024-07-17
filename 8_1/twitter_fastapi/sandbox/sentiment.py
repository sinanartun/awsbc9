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



def add_polarity_scores(df, text = "polarity_score"):
    sia = SentimentIntensityAnalyzer()
    
    df[text] = df["ytext"].apply(lambda x: 
        "bullish" if sia.polarity_scores(x)["compound"] > 0.2 else 
        "bearish" if sia.polarity_scores(x)["compound"] < -0.2 else 
        "neutral")
    return df


df = pd.read_csv("twitter_financial_news_sentiment_train.csv")
df = preprocess(df,"ytext")
df = add_polarity_scores(df)

# train_x, test_x, train_y, test_y = train_test_split(df["ytext"],
#                                                     df["Sentiment_Label"],
#                                                     random_state=42)

# # TF-IDF Word Level
# tf_idf_word_vectorizer = TfidfVectorizer().fit(train_x)
# x_train_tf_idf_word = tf_idf_word_vectorizer.transform(train_x)
# x_test_tf_idf_word = tf_idf_word_vectorizer.transform(test_x)

# rf_model = RandomForestClassifier().fit(x_train_tf_idf_word, train_y)
# cross_val_score(rf_model, x_test_tf_idf_word, test_y, cv=5, n_jobs=-1).mean()

# def prediction_random_from_dataset():
#     random_review = pd.Series(df["ytext"].sample(1).values)
#     new_comment = TfidfVectorizer().fit(train_x).transform(random_review)
#     pred = rf_model.predict(new_comment)
#     print(f'Review:  {random_review[0]} \n Prediction: {pred}')  
#     return    {"comment":random_review[0], 
#                "prediction":pred}  
    
# prediction_random_from_dataset()

# joblib.dump(rf_model, 'logistic_model.joblib')