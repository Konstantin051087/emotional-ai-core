import re
with open('app.py', 'r') as f:
    content = f.read()
    if 'port=5000' in content or 'PORT=5000' in content or ':5000' in content:
        print('✅ Порт приложения: 5000 (соответствует Render)')
    else:
        print('❌ Порт приложения не соответствует Render (требуется 5000)')
        exit(1)
