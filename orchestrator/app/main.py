# orchestrator/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time

from shared.schemas import ProcessRequest, ProcessResponse
from shared.config import Config
from app.utils.memory_manager import MemoryManager
from app.services.emotion_router import EmotionRouter
from app.services.personality_router import PersonalityRouter

from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="Emotional AI Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Метрики
REQUEST_COUNT = Counter('requests_total', 'Total requests')
RESPONSE_TIME = Histogram('response_time_seconds', 'Response time')
ERROR_COUNT = Counter('errors_total', 'Total errors')

# Сервисы
memory_manager = MemoryManager()
emotion_router = EmotionRouter()
personality_router = PersonalityRouter()

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    RESPONSE_TIME.observe(duration)
    REQUEST_COUNT.inc()
    return response

@app.post("/process", response_model=ProcessResponse)
async def process_message(request: ProcessRequest):
    try:
        # 1. Получаем контекст с памяти
        memory_context = await memory_manager.get_context(request.session_id)

        # 2. Параллельно анализируем: эмоции + личность + паттерны памяти
        emotion_task = emotion_router.analyze_emotion(request.user_input, memory_context)
        personality_task = personality_router.analyze_personality(request.user_input, memory_context)
        # memory patterns — можно расширить; текущая реализация возвращает словарь
        memory_patterns_task = memory_manager.get_patterns(request.session_id)

        emotion_state, personality_state, memory_patterns = await asyncio.gather(
            emotion_task, personality_task, memory_patterns_task
        )

        # 3. Генерируем ответ простым шаблонизатором (можно заменить на LLM later)
        response_text = emotion_router.generate_response(
            request.user_input, emotion_state, personality_state, memory_patterns, memory_context
        )

        # 4. Обновляем память
        await memory_manager.update_session(
            request.session_id,
            request.user_input,
            response_text,
            emotion_state.dict() if hasattr(emotion_state, "dict") else dict(emotion_state),
            personality_state.dict() if hasattr(personality_state, "dict") else dict(personality_state)
        )

        return ProcessResponse(
            response=response_text,
            emotional_state=emotion_state,
            personality_state=personality_state,
            memory_context=await memory_manager.get_context(request.session_id),
            confidence=calculate_confidence(emotion_state, personality_state)
        )

    except Exception as e:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "memory": await memory_manager.health_check(),
            "emotion_router": await emotion_router.health_check(),
            "personality_router": await personality_router.health_check()
        }
    }

@app.get("/metrics")
async def metrics():
    return generate_latest()

def calculate_confidence(emotion_state, personality_state):
    # emotion_state: model with .confidence
    emotion_confidence = getattr(emotion_state, "confidence", 0.5)
    neuro = getattr(personality_state, "neuroticism", 0.5)
    personality_stability = 1.0 - (neuro * 0.2)
    return round((emotion_confidence + personality_stability) / 2, 3)