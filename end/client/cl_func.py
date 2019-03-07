import sqlite3

conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
# cursor.execute("""create table if not exists ClientList
#                   (id int, nickname text, tgname text, id_chat text, message text)
#                """)
# cursor.execute("""create table if not exists Banner
#                   (firma text, text_b text, period int)
#                """)

# Создание таблиц
def start_defaullt():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("""create table if not exists ClientList
                      (id int, nickname text, tgname text, id_chat text, status text, message text)
                   """)
    cursor.execute("""create table if not exists Banner
                      (firma text, text_b text, period int)
                   """)
    conn.commit()


def insert_data (table_name, data): # данные в виде insert_data("ClientList", ''' '1', 'test', 'тест', 'f123', 'outside', 'hello AN' ''')
    sql = 'insert into ' + str(table_name) + ' values ( ' + str(data) + ' )'
    cursor.execute(sql)
    conn.commit()


def count ():
    cursor.execute('select count(*) from ClientList')
    count_l = cursor.fetchall()
    count_l = count_l[0][0]
    return count_l

def drop_data (table_name, num): # удаление выбывших
    sql = 'delete from ' + str(table_name) + ' where id = ' + str(num)
    cursor.execute(sql)
    conn.commit()
    # count_l = int(count())
    # for i in range(num+1, count_l):
    #     sql = 'update ' + str(table_name) + ' set number = ' + str(i-1) + ' where number = ' + str(i)
    #     cursor.execute(sql)
    # conn.commit()


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
    sql = 'select * from ClientList' # where id = 1
    cursor.execute(sql)
    row = cursor.fetchone()
    return row

def im_in(current_id):
    sql = '''update ClientList set status = 'inside' where id = ''' + str(current_id)
    cursor.execute(sql)
    pass