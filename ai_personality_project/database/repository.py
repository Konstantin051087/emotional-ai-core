import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from .db_config import DatabaseConfig
from .models import Conversation, TrainingData, ModelVersion

logger = logging.getLogger(__name__)

class EmotionalAIRepository:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.init_database()
    
    def init_database(self):
        """Инициализация таблиц базы данных"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            # Таблица разговоров
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL DEFAULT 'anonymous',
                    user_input TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    emotional_state JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица тренировочных данных
            cur.execute("""
                CREATE TABLE IF NOT EXISTS training_data (
                    id SERIAL PRIMARY KEY,
                    input_text TEXT NOT NULL,
                    expected_response TEXT NOT NULL,
                    emotional_context JSONB,
                    personality_traits JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица версий моделей
            cur.execute("""
                CREATE TABLE IF NOT EXISTS model_versions (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(50) UNIQUE NOT NULL,
                    model_path TEXT NOT NULL,
                    accuracy FLOAT DEFAULT 0.0,
                    training_data_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Индексы для оптимизации
            cur.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_training_data_created_at ON training_data(created_at)")
            
            conn.commit()
            cur.close()
            conn.close()
            logger.info("Таблицы базы данных успешно инициализированы")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации базы данных: {e}")
            raise
    
    def save_conversation(self, conversation: Conversation) -> int:
        """Сохранение разговора в базу данных"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO conversations (user_id, user_input, ai_response, emotional_state, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                conversation.user_id,
                conversation.user_input,
                conversation.ai_response,
                conversation.emotional_state,
                conversation.created_at
            ))
            
            conversation_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"Разговор сохранен с ID: {conversation_id}")
            return conversation_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения разговора: {e}")
            raise
    
    def get_conversation_history(self, user_id: str = "anonymous", limit: int = 50) -> List[Conversation]:
        """Получение истории разговоров пользователя"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT user_id, user_input, ai_response, emotional_state, created_at
                FROM conversations 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (user_id, limit))
            
            rows = cur.fetchall()
            conversations = []
            
            for row in rows:
                conversation = Conversation(
                    user_id=row[0],
                    user_input=row[1],
                    ai_response=row[2],
                    emotional_state=row[3] if row[3] else {},
                    created_at=row[4]
                )
                conversations.append(conversation)
            
            cur.close()
            conn.close()
            
            return conversations
            
        except Exception as e:
            logger.error(f"Ошибка получения истории разговоров: {e}")
            return []
    
    def save_training_data(self, training_data: TrainingData) -> int:
        """Сохранение тренировочных данных"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO training_data (input_text, expected_response, emotional_context, personality_traits, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                training_data.input_text,
                training_data.expected_response,
                training_data.emotional_context,
                training_data.personality_traits,
                training_data.created_at
            ))
            
            training_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"Тренировочные данные сохранены с ID: {training_id}")
            return training_id
            
        except Exception as e:
            logger.error(f"Ошибка сохранения тренировочных данных: {e}")
            raise
    
    def get_training_data(self, limit: int = 1000) -> List[TrainingData]:
        """Получение тренировочных данных"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT input_text, expected_response, emotional_context, personality_traits, created_at
                FROM training_data 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (limit,))
            
            rows = cur.fetchall()
            training_data_list = []
            
            for row in rows:
                training_data = TrainingData(
                    input_text=row[0],
                    expected_response=row[1],
                    emotional_context=row[2] if row[2] else {},
                    personality_traits=row[3] if row[3] else {},
                    created_at=row[4]
                )
                training_data_list.append(training_data)
            
            cur.close()
            conn.close()
            
            return training_data_list
            
        except Exception as e:
            logger.error(f"Ошибка получения тренировочных данных: {e}")
            return []
    
    def save_model_version(self, model_version: ModelVersion) -> bool:
        """Сохранение информации о версии модели"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO model_versions (version, model_path, accuracy, training_data_count, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (version) DO UPDATE SET
                    model_path = EXCLUDED.model_path,
                    accuracy = EXCLUDED.accuracy,
                    training_data_count = EXCLUDED.training_data_count,
                    created_at = EXCLUDED.created_at
            """, (
                model_version.version,
                model_version.model_path,
                model_version.accuracy,
                model_version.training_data_count,
                model_version.created_at
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"Информация о модели версии {model_version.version} сохранена")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения информации о модели: {e}")
            return False
    
    def get_latest_model_version(self) -> Optional[ModelVersion]:
        """Получение последней версии модели"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT version, model_path, accuracy, training_data_count, created_at
                FROM model_versions 
                ORDER BY created_at DESC 
                LIMIT 1
            """)
            
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if row:
                return ModelVersion(
                    version=row[0],
                    model_path=row[1],
                    accuracy=row[2],
                    training_data_count=row[3],
                    created_at=row[4]
                )
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения информации о модели: {e}")
            return None
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Получение статистики разговоров"""
        try:
            conn = self.db_config.get_connection()
            cur = conn.cursor()
            
            # Общее количество разговоров
            cur.execute("SELECT COUNT(*) FROM conversations")
            total_conversations = cur.fetchone()[0]
            
            # Количество уникальных пользователей
            cur.execute("SELECT COUNT(DISTINCT user_id) FROM conversations")
            unique_users = cur.fetchone()[0]
            
            # Количество тренировочных данных
            cur.execute("SELECT COUNT(*) FROM training_data")
            training_data_count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            return {
                'total_conversations': total_conversations,
                'unique_users': unique_users,
                'training_data_count': training_data_count,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}