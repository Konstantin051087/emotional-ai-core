from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from shared.config import Config

Base = declarative_base()

class SessionMemory(Base):
    __tablename__ = "session_memory"
    session_id = Column(String(255), primary_key=True)
    emotional_history = Column(JSON)
    conversation_history = Column(JSON)
    personality_profile = Column(JSON)
    memory_patterns = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MemoryManager:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    async def get_context(self, session_id: str):
        session = self.Session()
        try:
            memory = session.query(SessionMemory).filter_by(session_id=session_id).first()
            if not memory:
                return self._create_new_session(session_id)
            return {
                "session_id": session_id,
                "emotional_history": memory.emotional_history or [],
                "conversation_history": memory.conversation_history or [],
                "personality_profile": memory.personality_profile or {},
                "memory_patterns": memory.memory_patterns or {},
                "last_updated": memory.last_updated.isoformat()
            }
        finally:
            session.close()

    async def update_session(self, session_id: str, user_input: str, response: str, emotion_data: dict, personality_data: dict):
        session = self.Session()
        try:
            memory = session.query(SessionMemory).filter_by(session_id=session_id).first()
            if not memory:
                memory = SessionMemory(session_id=session_id)
                session.add(memory)
                memory.emotional_history = []
                memory.conversation_history = []
                memory.personality_profile = {}
                memory.memory_patterns = {}

            # Обновляем историю, профиль личности и паттерны памяти
            memory.emotional_history.append({"timestamp": datetime.utcnow().isoformat(), "emotion": emotion_data, "user_input": user_input})
            memory.conversation_history.append({"timestamp": datetime.utcnow().isoformat(), "user": user_input, "ai": response})
            memory.personality_profile.update(personality_data)
            memory.memory_patterns = self._update_memory_patterns(memory.memory_patterns, user_input, response, emotion_data)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def _create_new_session(self, session_id: str):
        return {
            "session_id": session_id,
            "emotional_history": [],
            "conversation_history": [],
            "personality_profile": {},
            "memory_patterns": {},
            "last_updated": datetime.utcnow().isoformat()
        }

    def _update_memory_patterns(self, patterns, user_input, response, emotion_data):
        emotion = emotion_data.get('primary_emotion', 'neutral')
        if 'emotion_patterns' not in patterns:
            patterns['emotion_patterns'] = {}
        patterns['emotion_patterns'][emotion] = patterns['emotion_patterns'].get(emotion, 0) + 1
        return patterns