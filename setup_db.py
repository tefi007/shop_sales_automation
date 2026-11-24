# -*- coding: utf-8 -*-
"""Создаёт рабочую базу данных и таблицы (запускается один раз)."""

import os
import psycopg2

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # чтобы работать из любой папки

from config import DB_CONFIG, DB_NAME


def main():
    # подключаемся к служебной базе и создаём рабочую, если её нет
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM pg_database WHERE datname = %s', (DB_NAME,))
    if cur.fetchone():
        print(f'База {DB_NAME} уже существует')
    else:
        cur.execute(f'CREATE DATABASE {DB_NAME}')
        print(f'Создана база {DB_NAME}')
    cur.close()
    conn.close()

    # создаём таблицы из sql/create_tables.sql
    db_config = dict(DB_CONFIG, dbname=DB_NAME)
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    with open('sql/create_tables.sql', encoding='utf-8') as f:
        cur.execute(f.read())
    conn.commit()
    print('Таблицы созданы (см. sql/create_tables.sql)')
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
