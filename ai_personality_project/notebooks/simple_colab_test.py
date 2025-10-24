#!/usr/bin/env python3
"""
Простой скрипт для тестирования в Google Colab
"""

print("🧠 AI Personality - Простой тест в Google Colab")
print("=" * 50)

# 1. Установка зависимостей
print("📦 Устанавливаем зависимости...")
try:
    import torch
    import transformers
    import gradio
    import matplotlib.pyplot as plt
    print("✅ Зависимости уже установлены")
except ImportError:
    print("⚠️ Устанавливаем зависимости...")
    import subprocess
    subprocess.run(["pip", "install", "torch", "transformers", "numpy", "matplotlib", "gradio"], check=True)
    print("✅ Зависимости установлены")

import sys
import os
import json
import numpy as np

# Добавляем текущую директорию в путь
sys.path.append('/content')

# 2. Тестирование профиля
print("\n👤 Тестируем профиль личности...")
try:
    with open('character_profile.json', 'r', encoding='utf-8') as f:
        profile = json.load(f)
    print(f"✅ Профиль загружен: {profile['name']}, {profile['age']} лет")
except Exception as e:
    print(f"❌ Ошибка загрузки профиля: {e}")

# 3. Тестирование эмоциональной модели
print("\n🧪 Тестируем эмоциональную модель...")
try:
    from emotional_model import EmotionalState
    model = EmotionalState()
    print("✅ Эмоциональная модель создана")
    
    # Простой тест
    test_text = "Я очень рад сегодняшнему дню!"
    result = model.update_from_text(test_text)
    print(f"✅ Тест пройден: настроение = {result['mood']}/10")
    
except Exception as e:
    print(f"❌ Ошибка эмоциональной модели: {e}")

# 4. Финальный отчет
print("\n" + "=" * 50)
print("🎯 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 50)
print("Следующие шаги:")
print("1. Загрузите файлы проекта в Colab")
print("2. Запустите полное тестирование")
print("3. Разверните на Hugging Face Spaces")
print("=" * 50)
