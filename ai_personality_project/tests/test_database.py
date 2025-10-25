import pytest
import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.repository import EmotionalAIRepository
from database.models import Conversation, TrainingData, ModelVersion

class TestDatabase:
    def setup_method(self):
        """Настройка тестовой базы данных"""
        self.repository = EmotionalAIRepository()
    
    def test_connection(self):
        """Тестирование подключения к базе данных"""
        assert self.repository.db_config.test_connection() == True
    
    def test_save_conversation(self):
        """Тестирование сохранения разговора"""
        conversation = Conversation(
            user_id="test_user",
            user_input="Тестовое сообщение",
            ai_response="Тестовый ответ",
            emotional_state={"mood": 5, "emotion": "neutral"}
        )
        
        conversation_id = self.repository.save_conversation(conversation)
        assert conversation_id > 0
    
    def test_get_conversation_history(self):
        """Тестирование получения истории разговоров"""
        conversations = self.repository.get_conversation_history("test_user", 10)
        assert isinstance(conversations, list)
    
    def test_save_training_data(self):
        """Тестирование сохранения тренировочных данных"""
        training_data = TrainingData(
            input_text="Тестовый ввод",
            expected_response="Тестовый ответ",
            emotional_context={"mood": 5},
            personality_traits={"openness": 8}
        )
        
        training_id = self.repository.save_training_data(training_data)
        assert training_id > 0
    
    def test_save_model_version(self):
        """Тестирование сохранения информации о модели"""
        model_version = ModelVersion(
            version="test_1.0",
            model_path="/test/path",
            accuracy=0.85,
            training_data_count=100
        )
        
        result = self.repository.save_model_version(model_version)
        assert result == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])