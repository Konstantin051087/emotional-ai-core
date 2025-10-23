import json
import jsonschema
from typing import Dict, List, Any

class ProfileValidator:
    def __init__(self):
        self.schema = {
            "type": "object",
            "required": ["name", "age", "background", "personality", "communication_style"],
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number", "minimum": 0, "maximum": 100},
                "background": {"type": "string", "minLength": 10},
                "personality": {
                    "type": "object",
                    "required": ["traits"],
                    "properties": {
                        "traits": {
                            "type": "object",
                            "required": ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"],
                            "properties": {
                                "openness": {"type": "number", "minimum": 0, "maximum": 10},
                                "conscientiousness": {"type": "number", "minimum": 0, "maximum": 10},
                                "extraversion": {"type": "number", "minimum": 0, "maximum": 10},
                                "agreeableness": {"type": "number", "minimum": 0, "maximum": 10},
                                "neuroticism": {"type": "number", "minimum": 0, "maximum": 10}
                            }
                        }
                    }
                }
            }
        }
    
    def validate_profile(self, profile_path: str) -> Dict[str, Any]:
        """Валидация профиля личности"""
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)
            
            jsonschema.validate(instance=profile, schema=self.schema)
            
            # Дополнительные проверки
            traits = profile['personality']['traits']
            total = sum(traits.values())
            
            return {
                "valid": True,
                "traits_total": total,
                "traits_balanced": 20 <= total <= 40,
                "messages": ["Профиль прошел валидацию"]
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "messages": ["Ошибка валидации профиля"]
            }

# Использование валидатора
if __name__ == "__main__":
    validator = ProfileValidator()
    result = validator.validate_profile("character_profile.json")
    print("Результат валидации:", result)