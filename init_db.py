import sqlite3


def create_db():
    conn = sqlite3.connect('preferences.db')
    cursor = conn.cursor()

    # Создание таблицы для хранения предпочтений пользователя
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_db()
