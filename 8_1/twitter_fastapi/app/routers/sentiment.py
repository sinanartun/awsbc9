from fastapi import APIRouter
from ..models.sentiment import Sentiment
from ..routers.clean import clean_text
from ..models.clean import Clean
from ..utils.predict import predict_sentiment

router = APIRouter()

@router.post("/sentiment/")
async def create_sentiment(sentiment: Sentiment):
    clean_data = Clean(text=sentiment.text)
    result = clean_text(clean_data)
    predicted_sentiment = predict_sentiment(result["text"])
    return {"text": result["text"], "sentiment": predicted_sentiment}
