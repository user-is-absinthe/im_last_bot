import sqlite3

# TODO: Собственные потоки
''''
def dostuff():
    with sql.connect("database.db") as con:
      name = "bob"
      cur = con.cursor()
      cur.execute("INSERT INTO students (name) VALUES (?)",(bob))
      con.commit()
      msg = "Done"
      
'''

def connector(sql, path = "mydatabase.db"):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        row = cursor.fetchone()
    return row


# conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
# cursor = conn.cursor()

# cursor.execute("""create table if not exists ClientList
#                   (id int, nickname text, tgname text, id_tg_user text, message text)
#                """)
# cursor.execute("""create table if not exists Banner
#                   (firma text, text_b text, period int)
#                """)

# Создание таблиц. Перед запуском измененной таблицы не забыть удалить старую базу
def start_defaullt(path = "mydatabase.db"):
    #conn = sqlite3.connect("mydatabase.db")
    # conn = sqlite3.connect(path)
    # cursor = conn.cursor()
    sql = """create table if not exists ClientList
                      (id int, nickname text, tgname text, id_tg_user text, status text, message text)
                   """
    connector(sql, path)
    sql = """create table if not exists Banner
                      (firma text, text_b text, period int)
                   """
    connector(sql, path)
    # cursor.execute("""create table if not exists ClientList
    #                   (id int, nickname text, tgname text, id_tg_user text, status text, message text)
    #                """)
    # cursor.execute("""create table if not exists Banner
    #                   (firma text, text_b text, period int)
    #                """)
    # conn.commit()

# TODO: Оповещение уже в тг-части. Триггер для Плотвы
def send_message(id_tg_user, message):
    pass

def insert_data (table_name, data, path): # данные в виде insert_data("ClientList", ''' '1', 'test', 'тест', 'f123', 'outside', 'hello AN' ''')
    sql = 'insert into ' + str(table_name) + ' values ( ' + str(data) + ' )'
    connector(sql,path)
    # cursor.execute(sql)
    # conn.commit()

def select_cl(id, path):
    sql = "select * from ClientList where id == "+ str(id)
    # cursor.execute(sql)
    row = connector(sql,path)#cursor.fetchone()
    return row

def select_cl_id_tg(id_tg, path):
    sql = "select * from ClientList where id_tg_user == "+ str(id_tg)
    # cursor.execute(sql)
    # row = cursor.fetchone()
    row = connector(sql,path)
    return row

def count (path = "mydatabase.db"):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('select count(*) from ClientList')
        count_l = cursor.fetchall()
        count_l = count_l[0][0]
    return count_l


def all_client (path = "mydatabase.db"):# список всех
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('select * from ClientList')
        rows = cursor.fetchall()
    return rows


def drop_client (id, path):# удаление, можно как бан
    id_tg_user = select_cl(id)[3]
    send_message(id_tg_user, 'you_go_away')
    sql = 'delete from ClientList where id = ' + str(id)
    connector(sql,path)
    # cursor.execute(sql)
    # conn.commit()
    # count_l = int(count())
    # if  count_l == 0:
    #     return 0
    # for i in range(id+1, count_l):
    #      sql = 'update ClientList set id = ' + str(i-1) + ' where id = ' + str(i)
    #      cursor.execute(sql)
    #      conn.commit()

def drop_client_tg_id (id_tg, path):
    send_message(id_tg, 'you_go_away')
    sql = 'delete from ClientList where id_tg_str = ' + str(id_tg)
    # cursor.execute(sql)
    # conn.commit()
    connector(sql,path)

def drop_all_cl (path): # очистка очереди
    for i in range (0,count()-1):
        id_tg_user = all_client()[i][3]
        send_message(id_tg_user, 'go_home')
    sql = 'delete from ClientList'
    connector(sql,path)
    # cursor.execute(sql)
    # conn.commit()

def prev_client (me_id, path = "mydatabase.db"):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
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

def count_before(me_id, path = "mydatabase.db"):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        sql = "select count(*) from ClientList where id < "+ str(me_id)
        cursor.execute(sql)
        count_l = cursor.fetchall()
        count_l = count_l[0][0]
        select_cl(me_id)[3]
    return count_l


def first_client (path):# первый
    sql = 'select * from ClientList' # where id = 1
    row = connector(sql,path)
    # cursor.execute(sql)
    # row = cursor.fetchone()
    return row

def im_in(current_id, path):#зашел на сдвчу
    sql = '''update ClientList set status = 'inside' where id = ''' + str(current_id)
    # cursor.execute(sql)
    # conn.commit()
    connector(sql,path)
    id_tg_user = select_cl(current_id)[3]
    send_message(id_tg_user, 'you_come_in')
    pass

def im_out(current_id, path):# вышел, запускайте следующего
    drop_client(current_id)
    send_message(str(first_client ()[3]), 'you_first')

def upd_message(id_tg,msg, path):
    sql = 'update ClientList set message ='+ str(msg) +'where id_tg_user = ' + str(id_tg)
    # cursor.execute(sql)
    # conn.commit()
    connector(sql,path)


# TODO: update username (by id)

def registr (path, id_tg_user, nickname=None, tgname=None, message=None): #registr('umnyj', 'neumnyj', '150319', 'там долго ещё?')
    status = 'outside'
    if count(path) > 0:
        id = str(all_client(path)[-1][0]+ 1)
    else:
        id = 1
    for i in range (0,count(path)-1):
        id_tg_user_t = all_client(path)[i][3]
        if id_tg_user == id_tg_user_t:
            send_message(id_tg_user, 'your_id_existed')
            return False
    data = '\'' + str(id) + '\', \'' + nickname + '\', \'' + tgname + '\', \'' + str(id_tg_user) + '\', \'' + status + '\', \'' + str(message) + '\''
    insert_data('ClientList', str(data), path)
    send_message(id_tg_user,'you_last')
    return True

