#!/usr/bin/env python3
"""
Тестирование функциональности для Hugging Face Spaces
"""

import sys
import os
import json

# Добавляем текущую директорию в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"📁 Текущая директория: {current_dir}")
print(f"📋 Файлы в директории: {os.listdir(current_dir)}")

def test_imports():
    """Тестирование импортов"""
    print("=== ТЕСТИРОВАНИЕ ИМПОРТОВ ===")
    
    try:
        import gradio as gr
        print("✅ Gradio установлен")
    except ImportError as e:
        print(f"❌ Ошибка импорта Gradio: {e}")
        return False
    
    try:
        # Прямой импорт из текущей директории
        from emotional_model import EmotionalState
        print("✅ EmotionalState импортирован")
    except ImportError as e:
        print(f"❌ Ошибка импорта EmotionalState: {e}")
        # Покажем полную трассировку для отладки
        import traceback
        traceback.print_exc()
        return False
    
    try:
        with open('character_profile.json', 'r', encoding='utf-8') as f:
            profile = json.load(f)
        print("✅ Профиль личности загружен")
        print(f"   Имя: {profile['name']}")
    except Exception as e:
        print(f"❌ Ошибка загрузки профиля: {e}")
        return False
    
    return True

def test_emotional_model():
    """Тестирование эмоциональной модели"""
    print("\n=== ТЕСТИРОВАНИЕ ЭМОЦИОНАЛЬНОЙ МОДЕЛИ ===")
    
    try:
        from emotional_model import EmotionalState
        
        model = EmotionalState()
        print("✅ Эмоциональная модель создана")
        
        # Тестовые фразы
        test_phrases = [
            "Я очень рад этому известию!",
            "Меня огорчили эти новости...",
            "Это вызывает у меня смешанные чувства."
        ]
        
        for phrase in test_phrases:
            state = model.update_from_text(phrase)
            print(f"✅ Фраза: '{phrase}'")
            print(f"   Настроение: {state['mood']}")
            print(f"   Доминирующая эмоция: {state['dominant_emotion']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования модели: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_functionality():
    """Тестирование функциональности приложения"""
    print("\n=== ТЕСТИРОВАНИЕ ПРИЛОЖЕНИЯ ===")
    
    try:
        # Проверяем, что app.py существует
        if not os.path.exists('app.py'):
            print("❌ Файл app.py не найден")
            return False
            
        # Импортируем класс приложения
        from app import AIPersonalityDemo
        
        demo = AIPersonalityDemo()
        print("✅ Демо-приложение инициализировано")
        
        # Тестовый анализ
        test_text = "Сегодня прекрасный день для новых начинаний!"
        result = demo.analyze_emotion(test_text)
        
        if result and isinstance(result, str) and len(result) > 0:
            print("✅ Анализ эмоций работает")
            print(f"   Результат содержит {len(result)} символов")
            print(f"   Первые 100 символов: {result[:100]}...")
        else:
            print("❌ Анализ эмоций не вернул ожидаемый результат")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования приложения: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования"""
    print("🧠 ТЕСТИРОВАНИЕ HUGGING FACE SPACES ДЕМО")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 3
    
    # Запуск тестов
    if test_imports():
        tests_passed += 1
    
    if test_emotional_model():
        tests_passed += 1
        
    if test_app_functionality():
        tests_passed += 1
    
    # Итоги
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Демо готово к развертыванию.")
        return True
    else:
        print("⚠️ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ. Требуется доработка.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)