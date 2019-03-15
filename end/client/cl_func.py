import sqlite3

conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
# cursor.execute("""create table if not exists ClientList
#                   (id int, nickname text, tgname text, id_chat text, message text)
#                """)
# cursor.execute("""create table if not exists Banner
#                   (firma text, text_b text, period int)
#                """)

# Создание таблиц. Перед запуском измененной таблицы не забыть удалить старую базу
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

# TODO: Оповещение уже в тг-части. Триггер для Плотвы
def send_message(id_chat):
    pass

def insert_data (table_name, data): # данные в виде insert_data("ClientList", ''' '1', 'test', 'тест', 'f123', 'outside', 'hello AN' ''')
    sql = 'insert into ' + str(table_name) + ' values ( ' + str(data) + ' )'
    cursor.execute(sql)
    conn.commit()


def count ():
    cursor.execute('select count(*) from ClientList')
    count_l = cursor.fetchall()
    count_l = count_l[0][0]
    return count_l

def drop_client (id):
    sql = 'delete from ClientList where id = ' + str(id)
    cursor.execute(sql)
    conn.commit()
    # count_l = int(count())
    # if  count_l == 0:
    #     return 0
    # for i in range(id+1, count_l):
    #      sql = 'update ClientList set id = ' + str(i-1) + ' where id = ' + str(i)
    #      cursor.execute(sql)
    #      conn.commit()

def drop_all_cl ():
    sql = 'delete from ClientList'
    cursor.execute(sql)
    conn.commit()

def prev_client (me_id):
    sql = "select * from ClientList where id == "+ str(me_id-1)
    cursor.execute(sql)
    row = cursor.fetchall()
    if len(row) == 0 and count() > 0:
        i = 2
        while len(row) == 0:
            sql = "select * from ClientList where id == " + str(me_id - i)
            cursor.execute(sql)
            row = cursor.fetchall()
            i = i +1
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
    conn.commit()
    pass

def im_out(current_id):
    drop_client(current_id)
    send_message(str(first_client ()[3]))

def registr (nickname, tgname, id_chat, message): #registr('umnyj', 'hujumnyj', '150319', 'сколько ещё под дверью сидеть?')
    status = 'outside'
    if count() > 0:
        id = str(all_client()[-1][0]+ 1)
    else:
        id = 1
    data = '\'' + str(id) + '\', \'' + nickname + '\', \'' + tgname + '\', \'' + str(id_chat) + '\', \'' + status + '\', \'' + message + '\''
    insert_data('ClientList', str(data))
    pass

