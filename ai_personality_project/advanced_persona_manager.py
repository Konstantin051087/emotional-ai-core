from advanced_emotional_model import AdvancedEmotionalModel
from ai_core import AICore
import json
from datetime import datetime

class AdvancedPersonaManager:
    def __init__(self):
        self.emotional_model = AdvancedEmotionalModel()
        self.ai_core = AICore()
        
        try:
            with open('character_profile.json', 'r', encoding='utf-8') as f:
                self.profile = json.load(f)
        except FileNotFoundError:
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
                }
            }
    
    def process_message(self, user_input: str):
        # Расширенный анализ сентимента
        sentiment = self.emotional_model.advanced_sentiment_analysis(user_input)
        
        # Обновление эмоционального состояния
        self.emotional_model.update_from_sentiment(sentiment)
        emotional_context = self.emotional_model.get_current_state()
        
        # Генерация контекстно-зависимого ответа
        response = self.ai_core.generate_response(user_input, emotional_context)
        
        # Логирование для анализа
        self._log_interaction(user_input, response, emotional_context)
        
        return response, emotional_context
    
    def _log_interaction(self, user_input: str, response: str, emotions: dict):
        """Логирование взаимодействий для последующего анализа"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "emotions": emotions
        }
        
        # Временное сохранение в файл (в Фазе 2 заменяется на базу данных)
        try:
            with open("conversation_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Ошибка логирования: {e}")
    
    def get_emotional_history(self):
        """Получение истории эмоциональных состояний"""
        return self.emotional_model.emotion_memory