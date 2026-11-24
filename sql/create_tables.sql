-- DDL для базы shop_sales.
-- Таблица чеков: одна строка = одна товарная позиция в чеке.

CREATE TABLE IF NOT EXISTS sales (
    id          SERIAL PRIMARY KEY,
    doc_id      TEXT NOT NULL,
    shop_num    INTEGER NOT NULL,
    cash_num    INTEGER NOT NULL,
    item        TEXT NOT NULL,
    category    TEXT NOT NULL,
    amount      INTEGER NOT NULL CHECK (amount > 0),
    price       NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    discount    NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (discount >= 0),
    sum_total   NUMERIC(10, 2) NOT NULL,  -- amount * price - discount
    loaded_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Уникальность позиции чека, чтобы повторный импорт того же файла не дублировал строки.
CREATE UNIQUE INDEX IF NOT EXISTS sales_doc_item_uidx
    ON sales (doc_id, shop_num, cash_num, item);
