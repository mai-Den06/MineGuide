import sqlite3

from config.setting import DB_PATH

def connect_db():
    """ データベースに接続する """
    return sqlite3.connect(DB_PATH)

def create_tables():
    """ テーブルを作成する（初回のみ実行） """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_visible BOOLEAN DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def insert_object(name, description):
    """ 物体データを挿入 """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO objects (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

def delete_object(name):
    """ 物体データを削除 """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM objects WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def set_visibility(name, is_visible):
    """ 物体の表示設定を変更 """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE objects SET is_visible = ? WHERE name = ?", (is_visible, name))
    conn.commit()
    conn.close()

def fetch_from_db(query, params):
    """共通のデータ取得関数"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()
    conn.close()
    return result[0] if result else "Not found"

def get_description(name):
    """物体名から概要を取得"""
    return fetch_from_db("SELECT description FROM objects WHERE name = ?", (name,))

def get_last_updated(name):
    """物体名から最終更新日時をUNIX時間で取得"""
    return fetch_from_db("SELECT strftime('%s', last_updated) FROM objects WHERE name = ?", (name,))

def get_is_visible(name):
    """物体名から表示設定を取得"""
    return fetch_from_db("SELECT is_visible FROM objects WHERE name = ?", (name,))
