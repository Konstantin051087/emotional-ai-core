# orchestrator/app/utils/memory_manager.py
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
        db_url = Config.DATABASE_URL or "sqlite:///./emotional_ai_local.db"
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    async def get_context(self, session_id: str):
        s = self.Session()
        try:
            mem = s.query(SessionMemory).filter_by(session_id=session_id).first()
            if not mem:
                return self._create_new_session(session_id)
            return {
                "session_id": session_id,
                "emotional_history": mem.emotional_history or [],
                "conversation_history": mem.conversation_history or [],
                "personality_profile": mem.personality_profile or {},
                "memory_patterns": mem.memory_patterns or {},
                "last_updated": mem.last_updated.isoformat() if mem.last_updated else datetime.utcnow().isoformat()
            }
        finally:
            s.close()

    async def update_session(self, session_id: str, user_input: str, response: str, emotion_data: dict, personality_data: dict):
        s = self.Session()
        try:
            mem = s.query(SessionMemory).filter_by(session_id=session_id).first()
            if not mem:
                mem = SessionMemory(session_id=session_id, emotional_history=[], conversation_history=[], personality_profile={}, memory_patterns={})
                s.add(mem)

            emotional_history = mem.emotional_history or []
            conversation_history = mem.conversation_history or []
            personality_profile = mem.personality_profile or {}
            memory_patterns = mem.memory_patterns or {}

            emotional_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "emotion": emotion_data,
                "user_input": user_input
            })
            if len(emotional_history) > Config.MAX_EMOTION_HISTORY:
                emotional_history = emotional_history[-Config.MAX_EMOTION_HISTORY:]

            conversation_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "user": user_input,
                "ai": response
            })
            if len(conversation_history) > Config.MAX_CONVERSATION_HISTORY:
                conversation_history = conversation_history[-Config.MAX_CONVERSATION_HISTORY:]

            # update personality history (simple append)
            for trait, value in (personality_data.items() if isinstance(personality_data, dict) else []):
                if trait not in personality_profile:
                    personality_profile[trait] = []
                personality_profile[trait].append(value)
                if len(personality_profile[trait]) > 10:
                    personality_profile[trait] = personality_profile[trait][-10:]

            memory_patterns = self._update_memory_patterns(memory_patterns, user_input, response, emotion_data)

            mem.emotional_history = emotional_history
            mem.conversation_history = conversation_history
            mem.personality_profile = personality_profile
            mem.memory_patterns = memory_patterns
            mem.last_updated = datetime.utcnow()

            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()

    async def get_patterns(self, session_id: str):
        s = self.Session()
        try:
            mem = s.query(SessionMemory).filter_by(session_id=session_id).first()
            return mem.memory_patterns if mem and mem.memory_patterns else {}
        finally:
            s.close()

    async def health_check(self):
        try:
            s = self.Session()
            s.execute("SELECT 1")
            s.close()
            return True
        except Exception:
            return False

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
        if patterns is None:
            patterns = {}
        emotion = emotion_data.get('primary_emotion') if isinstance(emotion_data, dict) else getattr(emotion_data, "primary_emotion", "neutral")
        if 'emotion_patterns' not in patterns:
            patterns['emotion_patterns'] = {}
        patterns['emotion_patterns'][emotion] = patterns['emotion_patterns'].get(emotion, 0) + 1
        return patterns
