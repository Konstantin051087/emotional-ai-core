import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseConfig:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'emotional_ai_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
    def get_connection(self):
        """Создание подключения к базе данных"""
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = False
            return conn
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise

    def test_connection(self):
        """Тестирование подключения к базе данных"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            cur.close()
            conn.close()
            logger.info(f"Успешное подключение к PostgreSQL: {db_version[0]}")
            return True
        except Exception as e:
            logger.error(f"Ошибка тестирования подключения: {e}")
            return False