import numpy as np
from datetime import datetime
from typing import Dict
from emotional_model import EmotionalState

class AdvancedEmotionalModel(EmotionalState):
    def __init__(self):
        super().__init__()
        self.emotion_memory = []  # История эмоциональных реакций
        self.long_term_tendencies = self._calculate_personality_tendencies()
    
    def _calculate_personality_tendencies(self) -> Dict[str, float]:
        """Расчет эмоциональных тенденций на основе черт личности"""
        traits = self.personality_traits
        
        return {
            "joy": traits["openness"] * 0.1 + traits["agreeableness"] * 0.05,
            "sadness": traits["neuroticism"] * 0.08,
            "anger": traits["neuroticism"] * 0.05 - traits["agreeableness"] * 0.03,
            "trust": traits["agreeableness"] * 0.1 + traits["conscientiousness"] * 0.02
        }
    
    def advanced_sentiment_analysis(self, text: str) -> Dict[str, float]:
        """Расширенный анализ с использованием моделей Hugging Face"""
        try:
            from transformers import pipeline
            sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="seara/rubert-tiny2-cedr-emotion-detection"
            )
            
            result = sentiment_analyzer(text)[0]
            label = result['label'].lower()
            score = result['score']
            
            # Маппинг результатов на наши эмоции
            emotion_map = {
                'радость': 'joy',
                'грусть': 'sadness', 
                'гнев': 'anger',
                'страх': 'fear',
                'доверие': 'trust'
            }
            
            if label in emotion_map:
                return {emotion_map[label]: score}
            else:
                return {"surprise": 0.3}  # Эмоция по умолчанию
                
        except ImportError:
            # Fallback на базовый анализ
            return self._basic_sentiment_analysis(text)
    
    def _basic_sentiment_analysis(self, text: str) -> Dict[str, float]:
        """Базовый анализ сентимента при отсутствии моделей"""
        positive_indicators = ["рад", "хорош", "прекрас", "любл", "нравится", "отлич", "счастлив"]
        negative_indicators = ["груст", "плох", "ужас", "ненавижу", "злю", "разочарован", "печал"]
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_indicators if word in text_lower)
        neg_count = sum(1 for word in negative_indicators if word in text_lower)
        
        total = max(pos_count + neg_count, 1)  # Избегаем деления на 0
        
        return {
            "joy": pos_count / total * 0.8,
            "sadness": neg_count / total * 0.7,
            "anger": neg_count / total * 0.3
        }