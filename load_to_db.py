# -*- coding: utf-8 -*-
"""Загружает выгрузки касс из папки data/ в базу shop_sales.

Берёт только файлы вида {{shop}}_{{cash}}.csv (например, 11_2.csv),
остальные файлы в папке игнорирует. Обработанные файлы переносит в data/processed/,
повторный импорт одного и того же файла не создаёт дублей (защита на уровне БД).
"""

import os
import re
import shutil
import csv
import psycopg2
from psycopg2.extras import execute_values

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # чтобы работать из любой папки

from config import DB_CONFIG, DB_NAME, DATA_DIR, PROCESSED_DIR

FILE_PATTERN = re.compile(r'^(\d+)_(\d+)\.csv$')  # shop_num_cash_num.csv


def parse_file(path, shop_num, cash_num):
    """Читает csv-выгрузку и возвращает строки для вставки."""
    rows = []
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            amount = int(r['amount'])
            price = float(r['price'])
            discount = float(r['discount'])
            rows.append((
                r['doc_id'], shop_num, cash_num, r['item'], r['category'],
                amount, price, discount,
                round(amount * price - discount, 2),  # sum_total
            ))
    return rows


def main():
    db_config = dict(DB_CONFIG, dbname=DB_NAME)
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    files = sorted(os.listdir(DATA_DIR))
    loaded, skipped = 0, 0
    for name in files:
        path = os.path.join(DATA_DIR, name)
        if not os.path.isfile(path):
            continue  # подпапки (например, processed) пропускаем
        if not FILE_PATTERN.match(name):
            skipped += 1
            continue  # лишний файл — игнорируем

        m = FILE_PATTERN.match(name)
        rows = parse_file(path, int(m.group(1)), int(m.group(2)))
        execute_values(cur, '''
            INSERT INTO sales
                (doc_id, shop_num, cash_num, item, category,
                 amount, price, discount, sum_total)
            VALUES %s
            ON CONFLICT (doc_id, shop_num, cash_num, item) DO NOTHING
        ''', rows)
        conn.commit()
        shutil.move(path, os.path.join(PROCESSED_DIR, name))
        print(f'Загружено {len(rows)} строк из {name}')
        loaded += 1

    print(f'Готово: обработано файлов — {loaded}, проигнорировано — {skipped}')
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
