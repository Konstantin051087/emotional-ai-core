from flask import Flask, render_template, request, jsonify, session
from advanced_persona_manager import AdvancedPersonaManager
from database.repository import EmotionalAIRepository
from database.models import Conversation, TrainingData
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'emotional-ai-secret-key-2024'

# Инициализация репозитория базы данных
db_repository = EmotionalAIRepository()

# Инициализация менеджера личности
persona_manager = AdvancedPersonaManager()

@app.before_request
def before_request():
    """Инициализация сессии пользователя"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session.permanent = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        user_id = session.get('user_id', 'anonymous')
        
        if not user_message.strip():
            return jsonify({'error': 'Пустое сообщение'}), 400
        
        # Обработка сообщения
        response, emotional_state = persona_manager.process_message(user_message)
        
        # Сохранение разговора в базу данных
        conversation = Conversation(
            user_id=user_id,
            user_input=user_message,
            ai_response=response,
            emotional_state=emotional_state
        )
        db_repository.save_conversation(conversation)
        
        # Сохранение тренировочных данных
        training_data = TrainingData(
            input_text=user_message,
            expected_response=response,
            emotional_context=emotional_state,
            personality_traits=persona_manager.profile.get('personality', {}).get('traits', {})
        )
        db_repository.save_training_data(training_data)
        
        return jsonify({
            'response': response,
            'emotional_state': emotional_state,
            'character_name': persona_manager.profile['name'],
            'user_id': user_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/character_info')
def character_info():
    """Информация о персонаже"""
    return jsonify(persona_manager.profile)

@app.route('/conversation_history')
def get_conversation_history():
    """Получение истории разговоров пользователя"""
    try:
        user_id = session.get('user_id', 'anonymous')
        limit = request.args.get('limit', 50, type=int)
        
        conversations = db_repository.get_conversation_history(user_id, limit)
        
        history_data = []
        for conv in conversations:
            history_data.append({
                'user_input': conv.user_input,
                'ai_response': conv.ai_response,
                'emotional_state': conv.emotional_state,
                'timestamp': conv.created_at.isoformat()
            })
        
        return jsonify({
            'user_id': user_id,
            'history': history_data,
            'total_count': len(history_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """Получение статистики"""
    try:
        stats = db_repository.get_conversation_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/training_data')
def get_training_data():
    """Получение тренировочных данных (только для администрирования)"""
    try:
        limit = request.args.get('limit', 100, type=int)
        training_data = db_repository.get_training_data(limit)
        
        training_list = []
        for data in training_data:
            training_list.append({
                'input_text': data.input_text,
                'expected_response': data.expected_response,
                'emotional_context': data.emotional_context,
                'personality_traits': data.personality_traits,
                'timestamp': data.created_at.isoformat()
            })
        
        return jsonify({
            'training_data': training_list,
            'total_count': len(training_list)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)