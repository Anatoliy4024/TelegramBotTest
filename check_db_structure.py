import sqlite3
import os

# Путь к базе данных
db_path = os.path.join(os.path.dirname(__file__), 'user_sessions.db')

# Подключение к базе данных
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Запрос на получение информации о столбцах таблицы user_sessions
c.execute('PRAGMA table_info(user_sessions)')
columns = c.fetchall()

# Вывод информации о столбцах
for column in columns:
    print(column)

conn.close()
