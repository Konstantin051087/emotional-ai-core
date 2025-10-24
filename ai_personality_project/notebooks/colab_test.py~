#!/usr/bin/env python3
"""
AI Personality - Тестирование Фазы 1 в Google Colab
Альтернативный скрипт для прямого запуска в Colab
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt

def setup_environment():
    """Настройка среды Colab"""
    print("🧠 AI Personality - Тестирование Фазы 1 в Google Colab")
    print("=" * 60)
    
    # Установка зависимостей
    print("📦 Установка зависимостей...")
    try:
        import torch
        import transformers
        import gradio
        print("✅ Зависимости уже установлены")
    except ImportError:
        print("⚠️ Устанавливаем зависимости...")
        os.system("pip install torch transformers numpy matplotlib gradio")
        print("✅ Зависимости установлены")
    
    # Настройка путей
    sys.path.append('/content')
    print("✅ Среда настроена")

def test_character_profile():
    """Тестирование профиля личности"""
    print("\n" + "=" * 40)
    print("👤 ТЕСТИРОВАНИЕ ПРОФИЛЯ ЛИЧНОСТИ")
    print("=" * 40)
    
    try:
        with open('character_profile.json', 'r', encoding='utf-8') as f:
            profile = json.load(f)
        
        print("✅ Профиль личности загружен успешно")
        print(f"   Имя: {profile['name']}")
        print(f"   Возраст: {profile['age']}")
        print(f"   Черты характера: {profile['personality']['traits']}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка загрузки профиля: {e}")
        return False

def test_emotional_model():
    """Тестирование эмоциональной модели"""
    print("\n" + "=" * 40)
    print("🧪 ТЕСТИРОВАНИЕ ЭМОЦИОНАЛЬНОЙ МОДЕЛИ")
    print("=" * 40)
    
    try:
        from emotional_model import EmotionalState
        
        # Создаем экземпляр модели
        emotional_model = EmotionalState()
        print("✅ Эмоциональная модель создана")
        
        # Тестовые фразы
        test_phrases = [
            "Я очень рад сегодняшним новостям! Это просто прекрасно!",
            "Меня расстроила эта ситуация, чувствую себя подавленно...",
            "Этот человек меня бесит, я в ярости от его поступка!",
            "Боюсь, что ничего не получится, страшно начинать новое дело.",
            "Я доверяю тебе и уверен в нашем сотрудничестве."
        ]
        
        print("\n🧪 Тестирование эмоциональных реакций:")
        for i, phrase in enumerate(test_phrases, 1):
            emotional_state = emotional_model.update_from_text(phrase)
            print(f"\n{i}. Фраза: '{phrase}'")
            print(f"   Настроение: {emotional_state['mood']}/10")
            print(f"   Доминирующая эмоция: {emotional_state['dominant_emotion']}")
            print(f"   Интенсивность: {emotional_state['dominant_intensity']:.2f}")
        
        return emotional_model
        
    except Exception as e:
        print(f"❌ Ошибка тестирования эмоциональной модели: {e}")
        import traceback
        traceback.print_exc()
        return None

def visualize_emotions(emotional_model):
    """Визуализация эмоционального состояния"""
    print("\n" + "=" * 40)
    print("📊 ВИЗУАЛИЗАЦИЯ ЭМОЦИОНАЛЬНОГО СОСТОЯНИЯ")
    print("=" * 40)
    
    try:
        emotional_summary = emotional_model.get_emotional_summary()
        emotions = emotional_summary['current_state']['emotions']
        
        # Создаем график
        plt.figure(figsize=(12, 6))
        
        # График эмоций
        plt.subplot(1, 2, 1)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        bars = plt.bar(emotions.keys(), emotions.values(), color=colors[:len(emotions)])
        plt.title('Эмоциональный профиль', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.ylabel('Интенсивность')
        plt.ylim(0, 1)
        
        # Добавляем значения на столбцы
        for bar, value in zip(bars, emotions.values()):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.2f}', ha='center', va='bottom')
        
        # График настроения
        plt.subplot(1, 2, 2)
        mood = emotional_summary['current_state']['mood']
        mood_color = '#4CAF50' if mood > 0 else '#F44336' if mood < 0 else '#FFC107'
        
        plt.bar(['Настроение'], [mood], color=mood_color)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.title(f'Настроение: {mood}/10', fontsize=14, fontweight='bold')
        plt.ylabel('Уровень настроения')
        plt.ylim(-10, 10)
        
        # Добавляем значение на столбец
        plt.text(0, mood + (0.5 if mood >= 0 else -0.8), f'{mood:.1f}', 
                 ha='center', va='bottom' if mood >= 0 else 'top', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
        
        print(f"📊 Сводка эмоционального состояния:")
        print(f"   Категория настроения: {emotional_summary['mood_category']}")
        print(f"   Эмоциональный тренд: {emotional_summary['emotional_trend']}")
        print(f"   Стабильность: {emotional_summary['current_state']['emotional_stability']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка визуализации: {e}")
        return False

def test_gradio_integration(emotional_model):
    """Тестирование интеграции с Gradio"""
    print("\n" + "=" * 40)
    print("🎭 ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ С GRADIO")
    print("=" * 40)
    
    try:
        import gradio as gr
        
        def test_emotion_analysis(text):
            """Тестовая функция для Gradio"""
            try:
                emotional_state = emotional_model.update_from_text(text)
                emotional_summary = emotional_model.get_emotional_summary()
                
                response = f"""
🧠 **Эмоциональный анализ:**

💬 **Текст:** {text}

📊 **Результаты:**
- Настроение: {emotional_state['mood']}/10 ({emotional_summary['mood_category']})
- Доминирующая эмоция: {emotional_state['dominant_emotion']}
- Интенсивность: {emotional_state['dominant_intensity']:.2f}
- Стабильность: {emotional_state['emotional_stability']:.2f}
- Тренд: {emotional_summary['emotional_trend']}

🕒 Анализ выполнен в Google Colab
                """
                return response
            except Exception as e:
                return f"Ошибка анализа: {e}"
        
        # Создаем простой интерфейс для тестирования
        demo = gr.Interface(
            fn=test_emotion_analysis,
            inputs=gr.Textbox(lines=3, placeholder="Введите текст для эмоционального анализа..."),
            outputs=gr.Markdown(),
            title="🧠 AI Personality - Тест в Google Colab",
            description="Тестирование эмоциональной модели в Google Colab среде"
        )
        
        print("✅ Gradio интерфейс создан")
        print("🚀 Запуск демо... (это может занять несколько секунд)")
        
        # Запускаем демо
        demo.launch(share=True, debug=True)
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования Gradio: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования"""
    setup_environment()
    
    # Запуск тестов
    test_results = {
        "profile_loaded": test_character_profile(),
        "emotional_model_working": False,
        "visualization_working": False,
        "gradio_integration": False
    }
    
    # Тестируем эмоциональную модель
    emotional_model = test_emotional_model()
    test_results["emotional_model_working"] = emotional_model is not None
    
    if emotional_model:
        test_results["visualization_working"] = visualize_emotions(emotional_model)
        # Комментируем Gradio тест для автоматического запуска
        # test_results["gradio_integration"] = test_gradio_integration(emotional_model)
    
    # Финальный отчет
    print("\n" + "=" * 60)
    print("🎯 ИТОГИ ТЕСТИРОВАНИЯ В GOOGLE COLAB")
    print("=" * 60)
    
    for test, result in test_results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}: {'ПРОЙДЕН' if result else 'НЕ ПРОЙДЕН'}")
    
    success_rate = sum(test_results.values()) / len(test_results) * 100
    print(f"\n📊 ОБЩИЙ РЕЗУЛЬТАТ: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🎉 ТЕСТИРОВАНИЕ ПРОЙДЕНО УСПЕШНО!")
        print("Фаза 1 готова к развертыванию на Hugging Face Spaces")
    else:
        print("⚠️ ТРЕБУЮТСЯ ДОРАБОТКИ!")
        print("Необходимо исправить указанные выше ошибки")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
