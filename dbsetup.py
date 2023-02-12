import enum 
import sqlite3
from lib.define import BLACK,WHITE
import lib.othello_utils as ou

DB_FILE_PATH = "./resource/othello.db"


CREATE_STAGE_TABLES_SQL = \
""" CREATE TABLE IF NOT EXISTS %s (
    id integer PRIMARY KEY,
    hash integer,
    hand bool,
    board_b text,
    board_w text,
    pass interger DEFAULT 0,
    status interger,
    duplicate_type interger,
    duplicate_stage_id integer,
    next_stages text
); """



# "000000 00000000 00000000 000000100 00001000 00000000 00000000 000000000"

def create_db(db_file_path):
    # データベースに接続
    conn = sqlite3.connect(db_file_path)

    # カーソルを取得
    cursor = conn.cursor()

    # SQL文を実行
    for idx in range(4,65):
        cursor.execute(CREATE_STAGE_TABLES_SQL % f"s{idx}")

    # 変更を保存
    conn.commit()

    # データベースとの接続を閉じる
    conn.close()

def seed(db_file_path):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    SEED_RECORD = \
    f"""
    INSERT INTO s4 (hash, hand, board_b, board_w) 
    SELECT ?, ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM s4 WHERE ID = 1);
    """
    board = ou.BORD_WB(w=int(0x0000000810000000),b=int(0x0000001008000000))
    cursor.execute(SEED_RECORD,(board.hash, BLACK, board.str_b, board.str_w))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db(DB_FILE_PATH)
    seed(DB_FILE_PATH)
    