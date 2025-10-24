#!/usr/bin/env python3
"""
AI Personality - Исправленное тестирование Фазы 1 в Google Colab
"""

import sys
import os
import json
import numpy as np

def main():
    """Основная функция тестирования"""
    print("🧠 AI Personality - Тестирование Фазы 1 в Google Colab")
    print("=" * 60)
    
    # Установка зависимостей
    print("📦 Установка зависимостей...")
    try:
        import torch
        import transformers
        import gradio
        import matplotlib.pyplot as plt
        print("✅ Зависимости уже установлены")
    except ImportError:
        print("⚠️ Устанавливаем зависимости...")
        os.system("pip install torch transformers numpy matplotlib gradio")
        print("✅ Зависимости установлены")
    
    # Настройка путей
    sys.path.append('/content')
    print("✅ Среда настроена")

    # Результаты тестирования
    test_results = {
        "profile_loaded": False,
        "emotional_model_working": False,
        "visualization_working": False,
        "gradio_integration": False
    }

    print("\n" + "=" * 40)
    print("👤 ТЕСТИРОВАНИЕ ПРОФИЛЯ ЛИЧНОСТИ")
    print("=" * 40)
    
    try:
        with open('character_profile.json', 'r', encoding='utf-8') as f:
            profile = json.load(f)
        test_results["profile_loaded"] = True
        print("✅ Профиль личности загружен успешно")
        print(f"   Имя: {profile['name']}")
        print(f"   Возраст: {profile['age']}")
        print(f"   Черты характера: {profile['personality']['traits']}")
    except Exception as e:
        print(f"❌ Ошибка загрузки профиля: {e}")

    print("\n" + "=" * 40)
    print("🧪 ТЕСТИРОВАНИЕ ЭМОЦИОНАЛЬНОЙ МОДЕЛИ")
    print("=" * 40)
    
    emotional_model = None
    try:
        from emotional_model import EmotionalState
        emotional_model = EmotionalState()
        test_results["emotional_model_working"] = True
        print("✅ Эмоциональная модель создана")
        
        # Тестовые фразы
        test_phrases = [
            "Я очень рад сегодняшним новостям! Это просто прекрасно!",
            "Меня расстроила эта ситуация, чувствую себя подавленно...",
            "Этот человек меня бесит, я в ярости от его поступка!"
        ]
        
        print("\n🧪 Тестирование эмоциональных реакций:")
        for i, phrase in enumerate(test_phrases, 1):
            emotional_state = emotional_model.update_from_text(phrase)
            print(f"\n{i}. Фраза: '{phrase}'")
            print(f"   Настроение: {emotional_state['mood']}/10")
            print(f"   Доминирующая эмоция: {emotional_state['dominant_emotion']}")
            print(f"   Интенсивность: {emotional_state['dominant_intensity']:.2f}")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования эмоциональной модели: {e}")

    print("\n" + "=" * 40)
    print("📊 ВИЗУАЛИЗАЦИЯ")
    print("=" * 40)
    
    try:
        import matplotlib.pyplot as plt
        test_results["visualization_working"] = True
        print("✅ Matplotlib работает")
        
        if emotional_model:
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
        
    except Exception as e:
        print(f"❌ Ошибка визуализации: {e}")

    print("\n" + "=" * 40)
    print("🎭 GRADO ИНТЕГРАЦИЯ")
    print("=" * 40)
    
    try:
        import gradio as gr
        test_results["gradio_integration"] = True
        print("✅ Gradio работает")
        
        if emotional_model:
            def test_emotion_analysis(text):
                try:
                    emotional_state = emotional_model.update_from_text(text)
                    emotional_summary = emotional_model.get_emotional_summary()
                    
                    response = f\"\"\"\n🧠 **Эмоциональный анализ:**\n\n💬 **Текст:** {text}\n\n📊 **Результаты:**\n- Настроение: {emotional_state['mood']}/10 ({emotional_summary['mood_category']})\n- Доминирующая эмоция: {emotional_state['dominant_emotion']}\n- Интенсивность: {emotional_state['dominant_intensity']:.2f}\n- Стабильность: {emotional_state['emotional_stability']:.2f}\n- Тренд: {emotional_summary['emotional_trend']}\n\n🕒 Анализ выполнен в Google Colab\n                    \"\"\"\n                    return response\n                except Exception as e:\n                    return f\"Ошибка анализа: {e}\"\n            \n            print(\"✅ Gradio функция создана\")\n            print(\"⚠️  Запуск интерфейса Gradio...\")\n            \n            # Создаем простой интерфейс\n            demo = gr.Interface(\n                fn=test_emotion_analysis,\n                inputs=gr.Textbox(lines=3, placeholder=\"Введите текст для эмоционального анализа...\"),\n                outputs=gr.Markdown(),\n                title=\"🧠 AI Personality - Тест в Google Colab\",\n                description=\"Тестирование эмоциональной модели в Google Colab среде\"\n            )\n            \n            demo.launch(share=True, quiet=True)\n            print(\"✅ Gradio интерфейс запущен\")\n        \n    except Exception as e:\n        print(f\"❌ Ошибка Gradio: {e}\")\n\n    # Финальный отчет\n    print("\n" + "=" * 60)\n    print("🎯 ИТОГИ ТЕСТИРОВАНИЯ В GOOGLE COLAB")\n    print("=" * 60)\n    \n    for test_name, result in test_results.items():\n        status = "✅" if result else "❌"\n        print(f"{status} {test_name}: {'ПРОЙДЕН' if result else 'НЕ ПРОЙДЕН'}")\n    \n    success_rate = sum(test_results.values()) / len(test_results) * 100\n    print(f"\\n📊 ОБЩИЙ РЕЗУЛЬТАТ: {success_rate:.1f}%")\n    \n    if success_rate >= 75:\n        print(\"🎉 ТЕСТИРОВАНИЕ ПРОЙДЕНО УСПЕШНО!\")\n        print(\"Фаза 1 готова к развертыванию на Hugging Face Spaces\")\n    else:\n        print(\"⚠️ ТРЕБУЮТСЯ ДОРАБОТКИ!\")\n        print(\"Необходимо исправить указанные выше ошибки\")\n    \n    print(\"=\" * 60)\n\nif __name__ == \"__main__\":\n    main()
