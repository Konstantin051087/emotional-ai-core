# orchestrator/shared/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "") or None
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    EMOTION_MODEL = os.getenv("EMOTION_MODEL", "j-hartmann/emotion-english-distilroberta-base")
    SENTIMENT_MODEL = os.getenv("SENTIMENT_MODEL", "cardiffnlp/twitter-roberta-base-sentiment-latest")

    EMOTION_MODULE_URL = os.getenv("EMOTION_MODULE_URL", "http://localhost:8001")
    PERSONALITY_MODULE_URL = os.getenv("PERSONALITY_MODULE_URL", "http://localhost:8002")
    MEMORY_MODULE_URL = os.getenv("MEMORY_MODULE_URL", "http://localhost:8003")

    MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", 50))
    MAX_EMOTION_HISTORY = int(os.getenv("MAX_EMOTION_HISTORY", 100))