#!/usr/bin/env python3
"""
Скрипт проверки Фазы 2
"""
from pathlib import Path
import sys
import os
import importlib

os.chdir('..')

def check_module(module_name):
    """Проверка наличия модуля"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}: ОК")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
        return False

def check_file(file_path):
    """Проверка наличия файла"""
    if os.path.exists(file_path):
        print(f"✅ {file_path}: ОК")
        return True
    else:
        print(f"❌ {file_path}: Отсутствует")
        return False

def main():
    """Основная функция проверки"""
    print("🔍 ПРОВЕРКА ФАЗЫ 2")
    print("=" * 50)
    
    # Проверка основных модулей
    modules = [
        'emotional_model',
        'advanced_emotional_model', 
        'ai_core',
        'advanced_persona_manager',
        'database.db_config',
        'database.models',
        'database.repository'
    ]
    
    files = [
        'character_profile.json',
        'requirements.txt',
        'app.py'
    ]
    
    modules_ok = 0
    files_ok = 0
    
    print("Проверка модулей:")
    for module in modules:
        if check_module(module):
            modules_ok += 1
    
    print("\nПроверка файлов:")
    for file in files:
        if check_file(file):
            files_ok += 1
    
    print("=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {modules_ok}/{len(modules)} модулей, {files_ok}/{len(files)} файлов")
    
    if modules_ok == len(modules) and files_ok == len(files):
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("Запуск приложения...")
        os.system("python app.py")
    else:
        print("⚠️ Требуется исправление ошибок")

if __name__ == "__main__":
    main()