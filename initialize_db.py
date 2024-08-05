import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'user_sessions.db')

def initialize_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Создание таблицы, если она не существует
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        language TEXT,
        telegram_name TEXT,
        user_name TEXT,
        event_date TEXT,
        start_time TEXT,
        end_time TEXT,
        duration INTEGER,
        number_of_people INTEGER,
        party_style TEXT,
        preferences TEXT,
        event_city TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print("Database and table created successfully.")
