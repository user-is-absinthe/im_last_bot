import sqlite3

conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""create table if not exists ClientList
                  (number int, nickname text, tgname text, id text, message text)
               """)
cursor.execute("""create table if not exists Banner
                  (firma text, text_b text, period int)
               """)