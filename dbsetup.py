import enum 
import sqlite3
from lib.define import BLACK,WHITE

DB_FILE_PATH = "./resource/othello.db"


CREATE_STAGE_TABLES_SQL = \
""" CREATE TABLE IF NOT EXISTS %s (
    id integer PRIMARY KEY,
    hand bool,
    board_b text,
    board_w text,
    pass interger DEFAULT 0,
    status interger,
    duplicate_type interger,
    duplicate_stage_id integer,
    next_stages text
); """

SEED_RECORD = \
f"""
INSERT INTO s4 (hand, board_b, board_w) 
SELECT ?, ?, ?
WHERE NOT EXISTS (SELECT 1 FROM s4 WHERE ID = 1);
"""

# "000000 00000000 00000000 000000100 00001000 00000000 00000000 000000000"

def create_db():
    # データベースに接続
    conn = sqlite3.connect(DB_FILE_PATH)

    # カーソルを取得
    cursor = conn.cursor()

    # SQL文を実行
    for idx in range(4,65):
        cursor.execute(CREATE_STAGE_TABLES_SQL % f"s{idx}")

    # 変更を保存
    conn.commit()

    # データベースとの接続を閉じる
    conn.close()

def seed():
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    cursor.execute(SEED_RECORD,(BLACK,str(int(0x0000001008000000)), str(int(0x0000000810000000))))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
    seed()
    