from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import sentiment

app = FastAPI()

# Configure CORS
origins = [
    "https://twitter.com",
    "https://x.com",
    "http://localhost",
    "http://localhost:8000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(sentiment.router)
