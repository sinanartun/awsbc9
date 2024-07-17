import joblib

# Load the pre-trained model and vectorizer
model = joblib.load('app/models/logistic_model.pkl')
vectorizer = joblib.load('app/models/tfidf_vectorizer.pkl')

def predict_sentiment(text: str):
    vectorized_text = vectorizer.transform([text])
    prediction = model.predict(vectorized_text)
    return prediction[0]
