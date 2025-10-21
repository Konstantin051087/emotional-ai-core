import aiohttp
from shared.schemas import EmotionAnalysis
from shared.config import Config

class EmotionRouter:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def analyze_emotion(self, text: str, context: dict) -> EmotionAnalysis:
        try:
            async with self.session.post(
                f"{Config.EMOTION_MODULE_URL}/analyze",
                json={"text": text, "context": context},
                timeout=10
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return EmotionAnalysis(**data)
                else:
                    return self._get_default_emotion()
        except Exception:
            return self._get_default_emotion()

    def _get_default_emotion(self):
        return EmotionAnalysis(
            primary_emotion="neutral",
            emotional_scores={"neutral": 1.0},
            intensity=0.5,
            confidence=0.5
        )