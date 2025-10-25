from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json

class AICore:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history_ids = None
        self.conversation_history = []
        
        # Загрузка профиля личности
        try:
            with open('character_profile.json', 'r', encoding='utf-8') as f:
                self.character_profile = json.load(f)
        except FileNotFoundError:
            self.character_profile = {
                "name": "Алиса",
                "age": 28,
                "background": "ИИ с эмоциональным интеллектом",
                "speech_style": "Дружелюбный и поддерживающий",
                "knowledge_base": ["психология", "технологии"]
            }
    
    def generate_response(self, user_input: str, emotional_context: dict = None) -> str:
        # Формирование промпта с учетом личности и эмоций
        prompt = self._build_prompt(user_input, emotional_context)
        
        # Кодирование ввода
        inputs = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors='pt')
        
        # Генерация ответа
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                top_k=50,
                top_p=0.9,
                temperature=0.8
            )
        
        # Декодирование ответа
        response = self.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        
        # Обновление истории
        self.conversation_history.append({"user": user_input, "ai": response})
        
        return response
    
    def _build_prompt(self, user_input: str, emotional_context: dict) -> str:
        """Построение промпта с учетом личности и эмоционального состояния"""
        base_prompt = f"""
        Ты {self.character_profile['name']}, {self.character_profile['age']} лет.
        Биография: {self.character_profile['background']}
        Черты характера: {self.character_profile['speech_style']}
        Знания: {', '.join(self.character_profile['knowledge_base'])}
        """
        
        if emotional_context:
            base_prompt += f"""
            Твое текущее настроение: {emotional_context['mood']}/10.
            Доминирующая эмоция: {emotional_context['dominant_emotion']}.
            Отвечай соответственно твоему эмоциональному состоянию.
            """
        
        base_prompt += f"\nПользователь: {user_input}\n{self.character_profile['name']}:"
        
        return base_prompt
    
    def reset_conversation(self):
        """Сброс истории разговора"""
        self.conversation_history = []
        self.chat_history_ids = None