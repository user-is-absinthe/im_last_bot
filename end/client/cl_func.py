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


def insert_data (table_name, data): # данные одной строкой через запятую по столбцам таблицы
    sql = 'insert into ' + str(table_name) + ' values ( ' + str(data) + ' )'
    cursor.execute(sql)
    pass

def count (type):
    cursor.execute('select count(*) from ClientList')
    count_list = cursor.fetchall()
    return count_list

def drop_data (table_name, num): # удаление выбывших и upgrade номеров
    sql = 'delete from ' + str(table_name) + ' where number = ' + str(num)
    cursor.execute(sql)
    count_l = int(count())
    for i in range(num+1, count_l):
        sql = 'update ' + str(table_name) + ' set number = ' + str(i-1) + ' where number = ' + str(i)
        cursor.execute(sql)

    pass



def prev_client (num):
    sql = "select * from ClientList where number == "+ str(num-1)
    cursor.execute(sql)
    row = cursor.fetchall()
    return row

def all_client ():
    cursor.execute('select * from ClientList')
    rows = cursor.fetchall()
    return rows

def first_client ():
    sql = "select * from ClientList where number = 1"
    cursor.execute(sql)
    row = cursor.fetchall()
    return row
