# orchestrator/app/services/emotion_router.py
import httpx
import random
from typing import Dict, Any

from shared.schemas import EmotionAnalysis, PersonalityState
from shared.config import Config

class EmotionRouter:
    def __init__(self):
        self.emotion_url = Config.EMOTION_MODULE_URL.rstrip("/")
        self.personality_url = Config.PERSONALITY_MODULE_URL.rstrip("/")

    async def analyze_emotion(self, text: str, context: Dict[str, Any]) -> EmotionAnalysis:
        # Вызов локального/удалённого emotion module
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(f"{self.emotion_url}/analyze", json={"text": text, "context": context})
                if r.status_code == 200:
                    data = r.json()
                    return EmotionAnalysis(**data)
        except Exception:
            pass
        # fallback
        return EmotionAnalysis(
            primary_emotion="neutral",
            emotional_scores={"neutral": 1.0},
            intensity=0.5,
            confidence=0.5
        )

    def generate_response(self, user_input: str, emotion_state: EmotionAnalysis,
                          personality_state: PersonalityState, memory_patterns: Dict[str, Any],
                          context: Dict[str, Any]) -> str:
        emotion = emotion_state.primary_emotion if hasattr(emotion_state, "primary_emotion") else "neutral"
        templates = {
            "joy": ["Это прекрасно! Рад слышать, что вы в хорошем настроении.", "Здорово! Продолжайте в том же духе!"],
            "anger": ["Понимаю ваше раздражение. Давайте разберемся спокойно."],
            "sadness": ["Мне жаль, что вам грустно. Хотите поговорить об этом?"],
            "fear": ["Понимаю ваше беспокойство. Давайте посмотрим на факты."],
            "disgust": ["Понимаю, что это неприятно."],
            "surprise": ["Неожиданно! Расскажите подробнее."],
            "neutral": ["Понятно. Расскажите подробнее.", "Интересно. Что вы об этом думаете?"]
        }
        choices = templates.get(emotion, templates["neutral"])
        resp = random.choice(choices)
        # небольшая персонализация
        if getattr(personality_state, "extraversion", 0.0) > 0.7:
            resp += " Кстати, расскажите подробнее — люблю живые истории!"
        elif getattr(personality_state, "neuroticism", 0.0) > 0.7:
            resp += " Надеюсь, всё наладится — поддерживаю вас."
        return resp

    async def health_check(self):
        # Проверка reachability модулей
        results = {"emotion_module": False, "personality_module": False}
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get(f"{self.emotion_url}/health")
                results["emotion_module"] = (r.status_code == 200)
        except Exception:
            results["emotion_module"] = False
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get(f"{self.personality_url}/health")
                results["personality_module"] = (r.status_code == 200)
        except Exception:
            results["personality_module"] = False
        return results