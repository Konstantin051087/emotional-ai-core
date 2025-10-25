import os
import json
from google.cloud import aiplatform
from google.cloud import storage
from typing import Dict, Any

class GCPConfig:
    def __init__(self):
        self.project_id = os.getenv('GCP_PROJECT_ID', 'emotional-ai-project')
        self.location = os.getenv('GCP_LOCATION', 'europe-west1')
        self.bucket_name = os.getenv('GCP_BUCKET_NAME', 'emotional-ai-models')
        self.staging_bucket = f"gs://{self.bucket_name}"
        
        # Инициализация клиентов
        self._init_clients()
    
    def _init_clients(self):
        """Инициализация клиентов Google Cloud"""
        try:
            # Инициализация AI Platform
            aiplatform.init(
                project=self.project_id,
                location=self.location,
                staging_bucket=self.staging_bucket
            )
            
            # Инициализация Cloud Storage
            self.storage_client = storage.Client(project=self.project_id)
            
            print("Google Cloud клиенты успешно инициализированы")
        except Exception as e:
            print(f"Ошибка инициализации Google Cloud: {e}")
            raise
    
    def create_bucket(self):
        """Создание бакета для хранения моделей"""
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            if not bucket.exists():
                bucket = self.storage_client.create_bucket(bucket, location=self.location)
                print(f"Бакет {self.bucket_name} создан")
            else:
                print(f"Бакет {self.bucket_name} уже существует")
            return bucket
        except Exception as e:
            print(f"Ошибка создания бакета: {e}")
            raise
    
    def upload_training_data(self, training_data_path: str, destination_blob_name: str):
        """Загрузка тренировочных данных в Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(destination_blob_name)
            
            blob.upload_from_filename(training_data_path)
            
            print(f"Файл {training_data_path} загружен в {destination_blob_name}")
            return f"gs://{self.bucket_name}/{destination_blob_name}"
        except Exception as e:
            print(f"Ошибка загрузки тренировочных данных: {e}")
            raise
    
    def download_model(self, source_blob_name: str, destination_file_name: str):
        """Скачивание модели из Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(source_blob_name)
            
            blob.download_to_filename(destination_file_name)
            
            print(f"Модель {source_blob_name} скачана в {destination_file_name}")
            return destination_file_name
        except Exception as e:
            print(f"Ошибка скачивания модели: {e}")
            raise