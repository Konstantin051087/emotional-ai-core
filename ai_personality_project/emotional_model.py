import json
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

class EmotionalState:
    def __init__(self, profile_path: str = "character_profile.json"):
        # Загрузка конфигурации из профиля
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
        except FileNotFoundError:
            # Фолбэк профиль если файл не найден
            self.profile = {
                "name": "Алиса",
                "personality": {
                    "traits": {
                        "openness": 9,
                        "conscientiousness": 7,
                        "extraversion": 3,
                        "agreeableness": 8,
                        "neuroticism": 4
                    }
                },
                "emotional_config": {
                    "base_sensitivity": 0.7,
                    "mood_swing_speed": 0.4,
                    "recovery_rate": 0.6
                }
            }
        
        # Инициализация эмоций
        self.emotions = {
            "joy": 0.5,
            "sadness": 0.2,
            "anger": 0.1,
            "fear": 0.1,
            "surprise": 0.3,
            "trust": 0.6,
            "anticipation": 0.4,
            "disgust": 0.1
        }
        
        # Настроение и состояние
        self.mood = 0.0  # -10 до +10
        self.arousal = 0.5  # 0 до 1 (активация)
        self.valence = 0.5  # 0 до 1 (позитивность)
        
        # История эмоций
        self.emotion_history = []
        self.last_update = datetime.now()
        
        # Конфигурация из профиля
        emotional_config = self.profile.get('emotional_config', {})
        self.sensitivity = emotional_config.get('base_sensitivity', 0.7)
        self.mood_swing_speed = emotional_config.get('mood_swing_speed', 0.4)
        self.recovery_rate = emotional_config.get('recovery_rate', 0.6)
    
    def update_from_text(self, text: str, sentiment_scores: Dict[str, float] = None):
        """Обновление эмоционального состояния на основе текста"""
        if sentiment_scores is None:
            sentiment_scores = self._analyze_sentiment_basic(text)
        
        # Применение чувствительности из профиля
        adjusted_scores = {
            emotion: score * self.sensitivity 
            for emotion, score in sentiment_scores.items()
        }
        
        # Обновление эмоций с учетом личности
        self._update_emotions_with_personality(adjusted_scores)
        
        # Расчет общего настроения
        self._calculate_mood()
        
        # Сохранение в историю
        self._save_to_history()
        
        return self.get_current_state()
    
    def _analyze_sentiment_basic(self, text: str) -> Dict[str, float]:
        """Базовая анализ сентимента текста"""
        text_lower = text.lower()
        
        # Эмоциональные словари
        emotion_lexicons = {
            "joy": [
                "рад", "счастлив", "восторг", "ура", "прекрасно", "отлично", 
                "люблю", "нравится", "восхитительно", "замечательно", "хорошо"
            ],
            "sadness": [
                "грустно", "печально", "тоска", "плачу", "разочарован", 
                "жаль", "скорбь", "уныние", "горе", "слезы", "плохо"
            ],
            "anger": [
                "злой", "сердит", "ярость", "гнев", "разозлился", "бесит",
                "ненавижу", "возмущен", "раздражен", "бешенство"
            ],
            "fear": [
                "боюсь", "страх", "испуг", "ужас", "опасно", "тревога",
                "паника", "напуган", "опасение", "беспокойство"
            ],
            "trust": [
                "доверяю", "уверен", "надежный", "верю", "доверие",
                "надежда", "уверенность", "надеюсь", "верный"
            ]
        }
        
        scores = {}
        for emotion, words in emotion_lexicons.items():
            count = sum(1 for word in words if word in text_lower)
            max_possible = len(words)
            scores[emotion] = count / max_possible if max_possible > 0 else 0
        
        return scores
    
    def _update_emotions_with_personality(self, sentiment_scores: Dict[str, float]):
        """Обновление эмоций с учетом черт личности"""
        traits = self.profile['personality']['traits']
        
        # Модификаторы на основе личности
        personality_modifiers = {
            "joy": traits['openness'] * 0.05 + traits['agreeableness'] * 0.03,
            "sadness": traits['neuroticism'] * 0.08,
            "anger": traits['neuroticism'] * 0.06 - traits['agreeableness'] * 0.04,
            "fear": traits['neuroticism'] * 0.07,
            "trust": traits['agreeableness'] * 0.08
        }
        
        # Применение затухания и новых влияний
        decay_rate = 1.0 - self.mood_swing_speed
        
        for emotion in self.emotions:
            base_decay = self.emotions[emotion] * decay_rate
            new_influence = sentiment_scores.get(emotion, 0) * self.mood_swing_speed
            personality_effect = personality_modifiers.get(emotion, 0)
            
            self.emotions[emotion] = base_decay + new_influence + personality_effect
            self.emotions[emotion] = max(0.0, min(1.0, self.emotions[emotion]))
    
    def _calculate_mood(self):
        """Расчет общего настроения"""
        positive_emotions = sum([
            self.emotions["joy"],
            self.emotions["trust"],
            self.emotions["surprise"] * 0.5,
            self.emotions["anticipation"] * 0.3
        ])
        
        negative_emotions = sum([
            self.emotions["sadness"],
            self.emotions["anger"], 
            self.emotions["fear"],
            self.emotions["disgust"]
        ])
        
        raw_mood = (positive_emotions - negative_emotions) * 10
        self.mood = max(-10.0, min(10.0, raw_mood))
        
        # Обновление валентности и активации
        self.valence = (self.mood + 10) / 20  # Нормализация к 0-1
        self.arousal = float(np.std(list(self.emotions.values())))  # Активация как дисперсия эмоций
    
    def _save_to_history(self):
        """Сохранение текущего состояния в историю"""
        state = self.get_current_state()
        state['timestamp'] = datetime.now().isoformat()
        self.emotion_history.append(state)
        
        # Ограничение размера истории
        if len(self.emotion_history) > 100:
            self.emotion_history.pop(0)
    
    def get_current_state(self) -> Dict[str, Any]:
        """Получение текущего эмоционального состояния"""
        dominant_emotion = max(self.emotions.items(), key=lambda x: x[1])
        
        return {
            "mood": round(self.mood, 2),
            "arousal": round(self.arousal, 3),
            "valence": round(self.valence, 3),
            "dominant_emotion": dominant_emotion[0],
            "dominant_intensity": round(dominant_emotion[1], 3),
            "emotions": {k: round(v, 3) for k, v in self.emotions.items()},
            "emotional_stability": round(1.0 - self.arousal, 3)  # Обратная активации
        }
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """Сводка эмоционального состояния"""
        current = self.get_current_state()
        
        return {
            "current_state": current,
            "mood_category": self._get_mood_category(current['mood']),
            "emotional_trend": self._get_emotional_trend(),
            "personality_influence": self._get_personality_influence()
        }
    
    def _get_mood_category(self, mood: float) -> str:
        """Категоризация настроения"""
        if mood >= 7: return "восторженное"
        elif mood >= 3: return "радостное" 
        elif mood >= 1: return "спокойное"
        elif mood >= -1: return "нейтральное"
        elif mood >= -3: return "задумчивое"
        elif mood >= -7: return "грустное"
        else: return "подавленное"
    
    def _get_emotional_trend(self) -> str:
        """Анализ тренда эмоций"""
        if len(self.emotion_history) < 2:
            return "стабильное"
        
        recent_moods = [state['mood'] for state in self.emotion_history[-5:]]
        if len(recent_moods) < 2:
            return "стабильное"
            
        try:
            x = list(range(len(recent_moods)))
            trend = np.polyfit(x, recent_moods, 1)[0]
            
            if trend > 0.5: return "улучшающееся"
            elif trend > 0.1: return "стабилизирующееся" 
            elif trend > -0.1: return "стабильное"
            elif trend > -0.5: return "ухудшающееся"
            else: return "резко ухудшающееся"
        except:
            return "стабильное"
    
    def _get_personality_influence(self) -> Dict[str, float]:
        """Влияние личности на эмоции"""
        traits = self.profile['personality']['traits']
        
        return {
            "openness_effect": traits['openness'] * 0.1,
            "neuroticism_effect": traits['neuroticism'] * 0.15,
            "agreeableness_effect": traits['agreeableness'] * 0.08
        }

# Тестовый код для проверки модуля
if __name__ == "__main__":
    print("🧠 Тестирование emotional_model.py")
    model = EmotionalState()
    test_text = "Я очень рад сегодняшнему дню!"
    result = model.update_from_text(test_text)
    print("Результат теста:", result)