import argparse
import os
import sys
from google.cloud import aiplatform
from datetime import datetime

def create_training_job(project_id: str, location: str, bucket_name: str):
    """Создание задания обучения на Google Cloud AI Platform"""
    
    # Инициализация
    aiplatform.init(project=project_id, location=location)
    
    # Конфигурация задания
    job_id = f"emotional_ai_train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Контейнер для обучения
    training_container = "gcr.io/cloud-aiplatform/training/tf-cpu.2-11:latest"
    
    # Аргументы для контейнера
    args = [
        "python", "training/trainer.py"
    ]
    
    # Создание задания
    job = aiplatform.CustomTrainingJob(
        display_name=job_id,
        container_uri=training_container,
        staging_bucket=f"gs://{bucket_name}",
    )
    
    # Запуск задания
    model = job.run(
        machine_type="n1-standard-4",
        args=args,
        replica_count=1,
    )
    
    print(f"✅ Задание обучения создано: {job_id}")
    return job

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True, help="Google Cloud Project ID")
    parser.add_argument("--location", default="europe-west1", help="GCP Location")
    parser.add_argument("--bucket-name", required=True, help="GCS Bucket name")
    
    args = parser.parse_args()
    
    try:
        job = create_training_job(
            args.project_id,
            args.location,
            args.bucket_name
        )
        print(f"Job created: {job}")
    except Exception as e:
        print(f"❌ Ошибка создания задания: {e}")

if __name__ == "__main__":
    main()