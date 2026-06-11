import sqlite3

def init_db():
    conn = sqlite3.connect("database/chat.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, message):
    conn = sqlite3.connect("database/chat.db")
    c = conn.cursor()

    c.execute("INSERT INTO chats (role, message) VALUES (?, ?)", (role, message))

    conn.commit()
    conn.close()