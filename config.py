# -*- coding: utf-8 -*-
"""Настройки подключения к базе данных и проекта."""

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'imoDuma#6#',  # пароль PostgreSQL на локальной машине
    'dbname': 'postgres',      # служебная база; рабочая создаётся скриптом setup_db.py
}

DB_NAME = 'shop_sales'
DATA_DIR = 'data'
PROCESSED_DIR = 'data/processed'
