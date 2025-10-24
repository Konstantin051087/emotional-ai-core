#!/usr/bin/env python3
"""
Скрипт для проверки валидности .ipynb файлов
"""

import json
import sys
import os

def validate_ipynb(file_path):
    """Проверка валидности .ipynb файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        print(f"✅ {file_path}: JSON валиден")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {file_path}: Ошибка JSON - {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path}: Ошибка - {e}")
        return False

def main():
    """Основная функция"""
    print("🔍 Проверка валидности .ipynb файлов")
    print("=" * 50)
    
    # Проверяем все .ipynb файлы в папке notebooks
    notebooks_dir = os.path.dirname(__file__)
    ipynb_files = [f for f in os.listdir(notebooks_dir) if f.endswith('.ipynb')]
    
    if not ipynb_files:
        print("❌ Не найдено .ipynb файлов")
        return False
    
    all_valid = True
    for ipynb_file in ipynb_files:
        file_path = os.path.join(notebooks_dir, ipynb_file)
        if not validate_ipynb(file_path):
            all_valid = False
    
    print("=" * 50)
    if all_valid:
        print("🎉 Все .ipynb файлы валидны!")
        return True
    else:
        print("⚠️ Некоторые файлы содержат ошибки")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
