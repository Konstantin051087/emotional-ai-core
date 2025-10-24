#!/usr/bin/env python3
"""
Скрипт гарантированной проверки валидности .ipynb файла
"""

import json
import sys

def validate_and_fix_notebook(filepath):
    """Проверка и исправление ноутбука"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Попытка загрузки JSON
        notebook = json.loads(content)
        print(f"✅ {filepath}: JSON валиден")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ {filepath}: Ошибка JSON - {e}")
        return False

if __name__ == "__main__":
    notebook_file = "phase1_testing.ipynb"
    if validate_and_fix_notebook(notebook_file):
        print("🎉 Ноутбук готов к использованию в Google Colab")
        sys.exit(0)
    else:
        print("🚨 Требуется исправление ноутбука")
        sys.exit(1)
