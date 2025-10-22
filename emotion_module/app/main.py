# modules/emotion_analyzer/app.py
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="Emotion Analysis Module (light)")

class AnalysisRequest(BaseModel):
    text: str
    context: dict = None

class AnalysisResponse(BaseModel):
    primary_emotion: str
    emotional_scores: dict
    intensity: float
    confidence: float

EMOTIONS = ["joy", "anger", "sadness", "fear", "disgust", "surprise", "neutral"]

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    # Простая эвристика: выбор эмоции по ключевым словам
    text = (request.text or "").lower()
    scores = {e: 0.0 for e in EMOTIONS}
    for kw, emo in [
        ("рад", "joy"), ("счаст", "joy"), ("люб", "joy"),
        ("злю", "anger"), ("бес", "anger"), ("ненав", "disgust"),
        ("грусть", "sadness"), ("груст", "sadness"), ("плак", "sadness"),
        ("боюсь", "fear"), ("тревог", "fear"), ("страх", "fear"),
        ("вау", "surprise"), ("неожид", "surprise")
    ]:
        if kw in text:
            scores[emo] += 0.8
    # Normalize to probabilities if no matches -> neutral
    if sum(scores.values()) == 0:
        scores["neutral"] = 1.0
    # ensure float probabilities
    total = sum(scores.values())
    normalized = {k: round(v / total, 3) for k, v in scores.items()}
    primary = max(normalized.items(), key=lambda x: x[1])[0]
    intensity = float(normalized[primary])
    # confidence: difference between top2
    sorted_vals = sorted(normalized.values(), reverse=True)
    confidence = float(sorted_vals[0] - (sorted_vals[1] if len(sorted_vals) > 1 else 0.0))
    return AnalysisResponse(
        primary_emotion=primary,
        emotional_scores=normalized,
        intensity=intensity,
        confidence=confidence
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": True}