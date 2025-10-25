FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание директорий
RUN mkdir -p logs trained_models

# Настройка переменных окружения
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]