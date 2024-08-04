import sqlite3

# Путь к базе данных
db_path = 'user_sessions.db'

# Устанавливаем соединение с базой данных
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Создаем таблицу user_sessions, если она не существует
c.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        start_time TEXT NOT NULL
    )
''')

# Проверяем существующие таблицы
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

# Закрываем соединение с базой данных
conn.close()

print("Database and table created successfully.")
