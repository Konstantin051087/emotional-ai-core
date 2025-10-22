from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="Personality Analysis Module")

class PersonalityRequest(BaseModel):
    text: str

class PersonalityResponse(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    dominant_trait: str

@app.post("/analyze", response_model=PersonalityResponse)
async def analyze_personality(request: PersonalityRequest):
    traits = {
        "openness": round(random.uniform(0, 1), 2),
        "conscientiousness": round(random.uniform(0, 1), 2),
        "extraversion": round(random.uniform(0, 1), 2),
        "agreeableness": round(random.uniform(0, 1), 2),
        "neuroticism": round(random.uniform(0, 1), 2)
    }
    dominant = max(traits, key=traits.get)

    return PersonalityResponse(**traits, dominant_trait=dominant)