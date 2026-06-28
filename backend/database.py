import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "clips.db"


def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DB_PATH)


def add_clip(platform, streamer, clip_id, title, url, vod_url):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clips (
            platform,
            streamer,
            clip_id,
            title,
            url,
            vod_url       
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        platform,
        streamer,
        clip_id,
        title,
        url,
        vod_url
    ))

    conn.commit()
    conn.close()

def clip_existe(clip_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM clips
        WHERE clip_id = ?
    """, (clip_id,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None

    
def get_pending_clips():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM clips
        WHERE status = 'pending'
    """)

    clips = cursor.fetchall()

    conn.close()

    return clips

def get_approved_clips():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM clips
        WHERE status = 'approved'
    """)

    clips = cursor.fetchall()

    conn.close()

    return clips

def get_downloaded_clips():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM clips
        WHERE status = 'downloaded'
    """)

    clips = cursor.fetchall()

    conn.close()

    return clips

def get_next_clip():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM clips
        WHERE status = 'pending'
        ORDER BY id
        LIMIT 1
    """)

    clip = cursor.fetchone()

    conn.close()

    return clip

def delete_clip_by_id(id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM clips WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

def update_clip_status(id, status):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clips
        SET status = ?
        WHERE id = ?
    """, (status, id))

    conn.commit()

    conn.close()


def get_clip_by_id(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM clips
        WHERE id = ?
    """, (id,))

    clip = cursor.fetchone()

    conn.close()

    return clip 


def add_streamer(platform, streamer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO streamers (
            platform,
            streamer
        )
        VALUES (?, ?)
    """, (platform, streamer))

    conn.commit()
    conn.close()


def get_streamers():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT platform, streamer
        FROM streamers
        WHERE active = 1
    """)

    streamers = cursor.fetchall()

    conn.close()

    return streamers

def delete_streamer(streamer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM streamers
        WHERE streamer = ?
    """, (streamer,))

    conn.commit()

    conn.close()

def delete_pending_clips_by_streamer(streamer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clips
        WHERE streamer = ?
        AND status = 'pending'
    """, (streamer,))

    conn.commit()

    conn.close()

def streamer_existe(streamer):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM streamers
        WHERE streamer = ?
    """, (streamer,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None

    
def adicionar_coluna_vod():

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""
            ALTER TABLE clips
            ADD COLUMN vod_url TEXT
        """)

        conn.commit()

    except sqlite3.OperationalError:
        pass

    conn.close

def criar_tabelas():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            streamer TEXT NOT NULL,
            clip_id TEXT UNIQUE,
            title TEXT,
            url TEXT,
            vod_url TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streamers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            streamer TEXT UNIQUE
        )
    """)

    conn.commit()

    conn.close()

criar_tabelas()

adicionar_coluna_vod()    
