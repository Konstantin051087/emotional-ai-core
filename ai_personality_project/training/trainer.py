import os
import sys
import json
import torch
import pandas as pd
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datetime import datetime
import logging

# Добавляем пути для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.repository import EmotionalAIRepository
from gcp.config import GCPConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionalAITrainer:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.db_repository = EmotionalAIRepository()
        self.gcp_config = GCPConfig()
        
        self.setup_model()
    
    def setup_model(self):
        """Загрузка и настройка модели"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Добавляем pad token если его нет
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Модель {self.model_name} успешно загружена")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            raise
    
    def prepare_training_data(self):
        """Подготовка тренировочных данных из базы данных"""
        try:
            training_data = self.db_repository.get_training_data(limit=5000)
            
            if not training_data:
                logger.warning("Нет тренировочных данных в базе данных")
                return None
            
            # Формируем промпты и ответы
            conversations = []
            for data in training_data:
                # Создаем промпт с учетом эмоционального контекста и личности
                prompt = self._build_prompt(
                    data.input_text, 
                    data.emotional_context, 
                    data.personality_traits
                )
                
                conversations.append({
                    'prompt': prompt,
                    'response': data.expected_response
                })
            
            logger.info(f"Подготовлено {len(conversations)} тренировочных примеров")
            return conversations
            
        except Exception as e:
            logger.error(f"Ошибка подготовки тренировочных данных: {e}")
            return None
    
    def _build_prompt(self, user_input: str, emotional_context: dict, personality_traits: dict) -> str:
        """Построение промпта с учетом эмоций и личности"""
        base_prompt = f"""
Ты {personality_traits.get('name', 'Алиса')}, ИИ с эмоциональным интеллектом.

Твои черты характера:
- Открытость: {personality_traits.get('openness', 7)}/10
- Добросовестность: {personality_traits.get('conscientiousness', 6)}/10
- Экстраверсия: {personality_traits.get('extraversion', 5)}/10
- Доброжелательность: {personality_traits.get('agreeableness', 8)}/10
- Невротизм: {personality_traits.get('neuroticism', 4)}/10

Твое текущее эмоциональное состояние:
- Настроение: {emotional_context.get('mood', 0)}/10
- Доминирующая эмоция: {emotional_context.get('dominant_emotion', 'нейтральное')}
"""
        
        prompt = f"{base_prompt}\n\nПользователь: {user_input}\nТы:"
        return prompt
    
    def tokenize_data(self, conversations):
        """Токенизация данных для обучения"""
        try:
            texts = []
            for conv in conversations:
                # Объединяем промпт и ответ
                full_text = f"{conv['prompt']} {conv['response']}{self.tokenizer.eos_token}"
                texts.append(full_text)
            
            # Токенизация
            tokenized = self.tokenizer(
                texts,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
            
            return tokenized
            
        except Exception as e:
            logger.error(f"Ошибка токенизации данных: {e}")
            raise
    
    def train(self, output_dir: str = "./trained_model"):
        """Запуск обучения модели"""
        try:
            # Подготовка данных
            conversations = self.prepare_training_data()
            if not conversations:
                logger.error("Не удалось подготовить данные для обучения")
                return False
            
            # Токенизация
            tokenized_data = self.tokenize_data(conversations)
            
            # Аргументы обучения
            training_args = TrainingArguments(
                output_dir=output_dir,
                overwrite_output_dir=True,
                num_train_epochs=3,
                per_device_train_batch_size=2,
                save_steps=500,
                save_total_limit=2,
                prediction_loss_only=True,
                remove_unused_columns=False,
                warmup_steps=100,
                logging_steps=10,
                learning_rate=5e-5,
                weight_decay=0.01,
            )
            
            # Коллатор данных
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,
            )
            
            # Создание тренера
            trainer = Trainer(
                model=self.model,
                args=training_args,
                data_collator=data_collator,
                train_dataset=tokenized_data,
            )
            
            # Запуск обучения
            logger.info("Начало обучения модели...")
            trainer.train()
            
            # Сохранение модели
            trainer.save_model()
            self.tokenizer.save_pretrained(output_dir)
            
            logger.info(f"Модель успешно обучена и сохранена в {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обучения модели: {e}")
            return False
    
    def upload_model_to_gcp(self, local_model_path: str, version: str = "1.0"):
        """Загрузка обученной модели в Google Cloud"""
        try:
            # Создание архива модели
            import shutil
            model_archive = f"emotional_ai_model_v{version}.tar.gz"
            shutil.make_archive(
                f"emotional_ai_model_v{version}", 
                'gztar', 
                local_model_path
            )
            
            # Загрузка в Cloud Storage
            gcs_path = self.gcp_config.upload_training_data(
                model_archive, 
                f"models/{model_archive}"
            )
            
            # Сохранение информации о модели в базу данных
            from database.models import ModelVersion
            model_version = ModelVersion(
                version=version,
                model_path=gcs_path,
                accuracy=0.85,  # Заглушка - в реальности нужно вычислять
                training_data_count=len(self.prepare_training_data() or [])
            )
            
            self.db_repository.save_model_version(model_version)
            
            logger.info(f"Модель загружена в Google Cloud: {gcs_path}")
            return gcs_path
            
        except Exception as e:
            logger.error(f"Ошибка загрузки модели в GCP: {e}")
            return None

def main():
    """Основная функция обучения"""
    try:
        trainer = EmotionalAITrainer()
        
        # Обучение модели
        if trainer.train():
            # Загрузка модели в Google Cloud
            version = f"1.{datetime.now().strftime('%Y%m%d%H%M')}"
            gcs_path = trainer.upload_model_to_gcp("./trained_model", version)
            
            if gcs_path:
                print(f"✅ Обучение завершено успешно! Модель сохранена: {gcs_path}")
            else:
                print("⚠️ Обучение завершено, но возникли проблемы с загрузкой в GCP")
        else:
            print("❌ Ошибка обучения модели")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()