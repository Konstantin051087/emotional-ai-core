    #!/usr/bin/env python3
"""
Скрипт проверки развертывания Фазы 2
"""

import sys
import os
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.repository import EmotionalAIRepository

os.chdir('..')

def check_database():
    """Проверка подключения к базе данных"""
    print("🔍 Проверка подключения к базе данных...")
    
    try:
        repository = EmotionalAIRepository()
        if repository.db_config.test_connection():
            print("✅ База данных: ОК")
            return True
        else:
            print("❌ База данных: Ошибка подключения")
            return False
    except Exception as e:
        print(f"❌ База данных: {e}")
        return False

def check_web_application():
    """Проверка веб-приложения"""
    print("🔍 Проверка веб-приложения...")
    
    try:
        # Тестируем локальный сервер
        response = requests.get('http://localhost:5000/', timeout=10)
        if response.status_code == 200:
            print("✅ Веб-приложение: ОК")
            return True
        else:
            print(f"❌ Веб-приложение: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Веб-приложение: {e}")
        return False

def check_api_endpoints():
    """Проверка API endpoints"""
    print("🔍 Проверка API endpoints...")
    
    endpoints = ['/character_info', '/stats']
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}: ОК")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
            return False
    
    return True

def main():
    """Основная функция проверки"""
    print("🚀 ПРОВЕРКА РАЗВЕРТЫВАНИЯ ФАЗЫ 2")
    print("=" * 50)
    
    checks = [
        check_database,
        check_web_application,
        check_api_endpoints
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print("=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {passed}/{total} проверок пройдено")
    
    if passed == total:
        print("🎉 ФАЗА 2 УСПЕШНО РАЗВЕРНУТА!")
        return True
    else:
        print("⚠️ Требуется исправление ошибок")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)