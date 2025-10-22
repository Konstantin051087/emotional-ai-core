# orchestrator/shared/schemas.py
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class EmotionAnalysis(BaseModel):
    primary_emotion: str
    emotional_scores: Dict[str, float]
    intensity: float
    confidence: float

class PersonalityState(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    dominant_trait: str

class MemoryContext(BaseModel):
    session_id: str
    emotional_history: List[Dict[str, Any]]
    conversation_history: List[Dict[str, str]]
    personality_profile: Dict[str, Any]
    last_updated: datetime

class ProcessRequest(BaseModel):
    user_input: str
    session_id: str
    context: Optional[Dict[str, Any]] = None

class ProcessResponse(BaseModel):
    response: str
    emotional_state: EmotionAnalysis
    personality_state: PersonalityState
    memory_context: MemoryContext
    confidence: float