from database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    streamer TEXT NOT NULL,
    clip_id TEXT NOT NULL,
    title TEXT,
    url TEXT,
    vod_url TEXT,
    status TEXT DEFAULT 'pending'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS streamers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    streamer TEXT NOT NULL UNIQUE,
    active INTEGER DEFAULT 1
)
""")

conn.commit()
conn.close()

print("Tabela criada com sucesso!")