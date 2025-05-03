import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    PROJECT_ID = os.getenv("PROJECT_ID")
    LOCATION = os.getenv("LOCATION", "us-central1")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-pro-preview-0409")
    CONTENT_JSON_PATH = "app/data/content.json"
