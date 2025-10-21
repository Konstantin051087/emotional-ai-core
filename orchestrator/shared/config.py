class Config:
    EMOTION_MODULE_URL = os.getenv("EMOTION_MODULE_URL", "http://localhost:8001")
    PERSONALITY_MODULE_URL = os.getenv("PERSONALITY_MODULE_URL", "http://localhost:8002")
    MEMORY_MODULE_URL = os.getenv("MEMORY_MODULE_URL", "http://localhost:8003")