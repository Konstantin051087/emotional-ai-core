from datetime import datetime
from typing import Dict, List, Any, Optional
import json

class Conversation:
    def __init__(self, 
                 user_id: str = "anonymous",
                 user_input: str = "",
                 ai_response: str = "",
                 emotional_state: Dict = None,
                 created_at: Optional[datetime] = None):
        self.user_id = user_id
        self.user_input = user_input
        self.ai_response = ai_response
        self.emotional_state = emotional_state or {}
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'user_input': self.user_input,
            'ai_response': self.ai_response,
            'emotional_state': json.dumps(self.emotional_state),
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        return cls(
            user_id=data.get('user_id', 'anonymous'),
            user_input=data.get('user_input', ''),
            ai_response=data.get('ai_response', ''),
            emotional_state=json.loads(data.get('emotional_state', '{}')),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )

class TrainingData:
    def __init__(self,
                 input_text: str = "",
                 expected_response: str = "",
                 emotional_context: Dict = None,
                 personality_traits: Dict = None,
                 created_at: Optional[datetime] = None):
        self.input_text = input_text
        self.expected_response = expected_response
        self.emotional_context = emotional_context or {}
        self.personality_traits = personality_traits or {}
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'input_text': self.input_text,
            'expected_response': self.expected_response,
            'emotional_context': json.dumps(self.emotional_context),
            'personality_traits': json.dumps(self.personality_traits),
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrainingData':
        return cls(
            input_text=data.get('input_text', ''),
            expected_response=data.get('expected_response', ''),
            emotional_context=json.loads(data.get('emotional_context', '{}')),
            personality_traits=json.loads(data.get('personality_traits', '{}')),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )

class ModelVersion:
    def __init__(self,
                 version: str = "1.0",
                 model_path: str = "",
                 accuracy: float = 0.0,
                 training_data_count: int = 0,
                 created_at: Optional[datetime] = None):
        self.version = version
        self.model_path = model_path
        self.accuracy = accuracy
        self.training_data_count = training_data_count
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': self.version,
            'model_path': self.model_path,
            'accuracy': self.accuracy,
            'training_data_count': self.training_data_count,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelVersion':
        return cls(
            version=data.get('version', '1.0'),
            model_path=data.get('model_path', ''),
            accuracy=data.get('accuracy', 0.0),
            training_data_count=data.get('training_data_count', 0),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )