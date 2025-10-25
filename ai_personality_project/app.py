#!/usr/bin/env python3
"""
Главный файл приложения для Hugging Face Spaces
Демонстрация эмоциональной модели ИИ
"""

import gradio as gr
import json
import sys
import os
from datetime import datetime

# Добавляем путь к текущей директории для импорта наших модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from emotional_model import EmotionalState
    EMOTIONAL_MODEL_AVAILABLE = True
except ImportError as e:
    print(f"Ошибка импорта emotional_model: {e}")
    EMOTIONAL_MODEL_AVAILABLE = False

class AIPersonalityDemo:
    def __init__(self):
        """Инициализация демо-приложения"""
        self.profile = self._load_profile()
        self.emotional_model = None
        self.initialize_model()
        
    def _load_profile(self):
        """Загрузка профиля личности"""
        try:
            with open('character_profile.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки профиля: {e}")
            return {
                "name": "Алиса",
                "age": 28,
                "background": "ИИ с эмоциональным интеллектом"
            }
    
    def initialize_model(self):
        """Инициализация эмоциональной модели"""
        if EMOTIONAL_MODEL_AVAILABLE:
            try:
                self.emotional_model = EmotionalState()
                print("Эмоциональная модель успешно инициализирована")
            except Exception as e:
                print(f"Ошибка инициализации модели: {e}")
                self.emotional_model = None
        else:
            print("Эмоциональная модель недоступна")
    
    def analyze_emotion(self, user_text):
        """
        Анализ текста и возврат эмоциональной реакции
        
        Args:
            user_text (str): Текст пользователя
            
        Returns:
            dict: Результаты анализа
        """
        if not user_text or not user_text.strip():
            return self._format_response("Пожалуйста, введите текст для анализа", {})
        
        try:
            if self.emotional_model:
                # Анализ эмоций
                emotional_state = self.emotional_model.update_from_text(user_text)
                emotional_summary = self.emotional_model.get_emotional_summary()
                
                # Форматирование ответа
                response_text = self._format_ai_response(user_text, emotional_state, emotional_summary)
                return response_text
            else:
                return self._format_response(
                    "Эмоциональная модель временно недоступна", 
                    {"error": "model_not_available"}
                )
                
        except Exception as e:
            print(f"Ошибка анализа: {e}")
            return self._format_response(
                "Произошла ошибка при анализе текста", 
                {"error": str(e)}
            )
    
    def _format_ai_response(self, user_text, emotional_state, emotional_summary):
        """Форматирование ответа ИИ"""
        # Базовые ответы в зависимости от настроения
        mood_responses = {
            "восторженное": "Я чувствую невероятный подъем!",
            "радостное": "Мне очень приятно это слышать!",
            "спокойное": "Я воспринимаю это спокойно.",
            "нейтральное": "Я анализирую эту информацию.",
            "задумчивое": "Это заставляет меня задуматься...",
            "грустное": "Мне немного грустно от этого.",
            "подавленное": "Это вызывает у меня тяжелые чувства."
        }
        
        mood_category = emotional_summary.get('mood_category', 'нейтральное')
        base_response = mood_responses.get(mood_category, "Я размышляю над этим.")
        
        # Детали эмоционального анализа
        emotion_details = f"""
### 🧠 Эмоциональный анализ

**Настроение:** {emotional_state['mood']}/10 ({mood_category})  
**Доминирующая эмоция:** {emotional_state['dominant_emotion']}  
**Интенсивность:** {emotional_state['dominant_intensity']:.2f}  
**Стабильность:** {emotional_state['emotional_stability']:.2f}  
**Тренд:** {emotional_summary.get('emotional_trend', 'стабильное')}

### 📊 Детали эмоций:
"""
        
        # Добавляем все эмоции
        for emotion, intensity in emotional_state['emotions'].items():
            emotion_icon = self._get_emotion_icon(emotion)
            emotion_details += f"{emotion_icon} **{emotion}:** {intensity:.2f}\n"
        
        full_response = f"""
{base_response}

{emotion_details}

---
*Анализ выполнен: {datetime.now().strftime('%H:%M:%S')}*
"""
        return full_response
    
    def _format_response(self, message, data):
        """Форматирование простого ответа"""
        return f"""
### {message}

{json.dumps(data, ensure_ascii=False, indent=2) if data else ''}
"""
    
    def _get_emotion_icon(self, emotion):
        """Получение иконки для эмоции"""
        icons = {
            "joy": "😊",
            "sadness": "😢", 
            "anger": "😠",
            "fear": "😨",
            "surprise": "😲",
            "trust": "🤝",
            "anticipation": "👀",
            "disgust": "🤢"
        }
        return icons.get(emotion, "•")

def create_demo_interface():
    """Создание интерфейса Gradio"""
    demo = AIPersonalityDemo()
    
    # Информация о персонаже
    character_info = f"""
    ## 👤 {demo.profile['name']}, {demo.profile['age']} лет
    
    **Биография:** {demo.profile.get('background', 'ИИ с развитым эмоциональным интеллектом')}
    
    **Черты характера:**
    - Открытость: {demo.profile['personality']['traits']['openness']}/10
    - Добросовестность: {demo.profile['personality']['traits']['conscientiousness']}/10  
    - Экстраверсия: {demo.profile['personality']['traits']['extraversion']}/10
    - Доброжелательность: {demo.profile['personality']['traits']['agreeableness']}/10
    - Невротизм: {demo.profile['personality']['traits']['neuroticism']}/10
    """
    
    with gr.Blocks(
        title="AI Personality Demo",
        theme=gr.themes.Soft(),
        css="""
        .emotion-bar { 
            background: linear-gradient(90deg, #4CAF50, #FFC107, #F44336); 
            height: 20px; 
            border-radius: 10px; 
            margin: 5px 0; 
        }
        .positive { color: #4CAF50; }
        .negative { color: #F44336; }
        .neutral { color: #FFC107; }
        """
    ) as interface:
        
        gr.Markdown("# 🧠 AI Personality - Демо эмоционального интеллекта")
        gr.Markdown("Демонстрация антропоморфного ИИ с личностью и эмоциональными реакциями")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(character_info)
                gr.Markdown("### 📝 Примеры для тестирования:")
                examples = gr.Examples(
                    examples=[
                        ["Я получил повышение на работе! Очень рад этому событию!"],
                        ["Сегодня грустный день, потерял важные документы..."],
                        ["Этот проект вызывает у меня смешанные чувства и некоторую тревогу."],
                        ["Я уверен, что у нас все получится! Мы отлично поработали."],
                        ["Меня разозлило это несправедливое решение."]
                    ],
                    inputs=gr.Textbox(label="Введите текст")
                )
                
            with gr.Column(scale=2):
                with gr.Group():
                    input_text = gr.Textbox(
                        label="💬 Введите текст для эмоционального анализа",
                        placeholder="Напишите что-нибудь, и Алиса проанализирует эмоциональную окраску...",
                        lines=3,
                        max_lines=5
                    )
                    
                    analyze_btn = gr.Button("Анализировать эмоции 🎭", variant="primary")
                
                output_text = gr.Markdown(
                    label="📊 Результаты эмоционального анализа",
                    value="### Жду ваше сообщение для анализа...\n\nЗдесь появится детальный анализ эмоциональной окраски вашего текста."
                )
        
        # Обработчики событий
        analyze_btn.click(
            fn=demo.analyze_emotion,
            inputs=input_text,
            outputs=output_text
        )
        
        input_text.submit(
            fn=demo.analyze_emotion,
            inputs=input_text,
            outputs=output_text
        )
        
        # Дополнительная информация
        with gr.Accordion("ℹ️ О проекте", open=False):
            gr.Markdown("""
            **AI Personality Project** - исследовательский проект по созданию антропоморфного ИИ.
            
            **Технологии:**
            - Python 3.11
            - PyTorch + Transformers
            - Gradio для интерфейса
            - Hugging Face Spaces для хостинга
            
            **Ресурсы разработки:**
            - GitHub Codespaces - среда разработки
            - Google Colab - тестирование моделей
            - GitHub - контроль версий
            - Render - бэкенд хостинг
            
            **Текущая версия:** 1.0 (Фаза 1: Проектирование)
            """)
    
    return interface

# Создание и запуск интерфейса
if __name__ == "__main__":
    interface = create_demo_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=5000,
        share=False,
        debug=True
    )