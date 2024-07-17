from pydantic import BaseModel

class Sentiment(BaseModel):
    text: str
