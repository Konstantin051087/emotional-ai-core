# orchestrator/app/services/personality_router.py
import httpx
from typing import Dict, Any
from shared.schemas import PersonalityState
from shared.config import Config

class PersonalityRouter:
    def __init__(self):
        self.personality_url = Config.PERSONALITY_MODULE_URL.rstrip("/")

    async def analyze_personality(self, text: str, context: Dict[str, Any]) -> PersonalityState:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(f"{self.personality_url}/analyze", json={"text": text, "context": context})
                if r.status_code == 200:
                    data = r.json()
                    return PersonalityState(**data)
        except Exception:
            pass

        # fallback neutral personality
        return PersonalityState(
            openness=0.5,
            conscientiousness=0.5,
            extraversion=0.5,
            agreeableness=0.5,
            neuroticism=0.5,
            dominant_trait="neutral"
        )

    async def health_check(self):
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get(f"{self.personality_url}/health")
                return r.status_code == 200
        except Exception:
            return False