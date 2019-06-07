import sqlite3

#from tiny_client import test_another_pytelegrambotapi as tg_api

PATH_DEFAULLT = 'mydatabase.db'

def connector(sql, path = PATH_DEFAULLT):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        row = cursor.fetchone()
    return row


# Создание таблиц. Перед запуском измененной таблицы не забыть удалить старую базу
def start_defaullt(path = PATH_DEFAULLT):
    sql = """create table if not exists ClientList
                      (id_tg_user integer PRIMARY KEY,
                      num_id integer,
                      nickname text,
                      tgname text,
                      status text,
                      message text);
                   """
    connector(sql, path)
    # sql = """create table if not exists Banner
    #                   (id integer PRIMARY KEY,
    #                   firma text,
    #                   text_banner text,
    #                   period int);
    #                """
    # connector(sql, path)
    return True

# TODO: Оповещение уже в тг-части. Триггер для Плотвы
def send_message(id_tg_user, message):
    # tg_api.random_message(
    #     id_tg_user=id_tg_user,
    #     text_message=message
    # )
    pass

def insert_data (table_name, data, path = PATH_DEFAULLT):
    sql = 'insert into ' + str(table_name) + ' values ( ' + str(data) + ' )'
    connector(sql,path)
    return True

def select_cl_id_tg(id_tg, path = PATH_DEFAULLT):
    sql = "select * from ClientList where id_tg_user = "+ str(id_tg)
    row = connector(sql,path)
    return row

def count (path = PATH_DEFAULLT):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('select count(*) from ClientList')
        count_l = cursor.fetchall()
        count_l = count_l[0][0]
    return count_l


def all_client (path = PATH_DEFAULLT):# список всех
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('select * from ClientList')
        rows = cursor.fetchall()
    return rows


def drop_client_tg_id (id_tg, path = PATH_DEFAULLT):
    send_message(id_tg, 'you_go_away')
    sql = 'delete from ClientList where id_tg_user = ' + str(id_tg)
    connector(sql,path)
    return True

def drop_all_cl (path= PATH_DEFAULLT): # очистка очереди
    for i in range (0,count()-1):
        id_tg_user = all_client()[i][0]
        send_message(id_tg_user, 'go_home')
    #sql = 'delete from ClientList'
    sql = 'DROP TABLE ClientList'
    connector(sql,path)
    start_defaullt(path)
    return True


def prev_client (id_tg_user, path = PATH_DEFAULLT):
    if count(path) ==1:
        return False
    sql = "select num_id from ClientList where id_tg_user = " + str(id_tg_user)
    num_id = int(connector(sql, path)[0])
    sql = "select * from ClientList where num_id < "+ str(num_id) + " ORDER BY num_id DESC"
    row = connector(sql, path)
    return row


def count_before(id_tg_user, path = PATH_DEFAULLT):
    sql = "select num_id from ClientList where id_tg_user = "+ str(id_tg_user)
    num_id = connector(sql, path)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('select count(*) from ClientList where num_id < ?', num_id)
        count_l = cursor.fetchall()
        count_l = count_l[0][0]
    return count_l

def first_client (path = PATH_DEFAULLT):# первый
    sql = 'select * from ClientList' # where id = 1
    row = connector(sql,path)
    # cursor.execute(sql)
    # row = cursor.fetchone()
    return row

def im_in(id_tg_user, path = PATH_DEFAULLT) :#зашел на сдвчу
    sql = '''select  id_tg_user from ClientList where status = "inside"'''
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        in_list = cursor.fetchall()
    if in_list is not None:
        for id_u in in_list:
            drop_client_tg_id(id_u[0],path)

    sql = '''update ClientList set status = 'inside' where id_tg_user = ''' + str(id_tg_user)
    # cursor.execute(sql)
    # conn.commit()
    connector(sql,path)
    send_message(id_tg_user, 'you_come_in')
    return True

# def im_out(id_tg_user, path= PATH_DEFAULLT):# вышел, запускайте следующего
#     sql = 'select status from ClientList WHERE id_tg_user =' + str(id_tg_user)
#     status = connector(sql, path)[0]
#     if status == 'inside':
#         drop_client_tg_id(id_tg_user)
#         send_message(str(first_client ()[0]), 'you_first')
#         return True
#     else:
#         return False

def upd_message(id_tg, msg,  path = PATH_DEFAULLT):#upd_message((150319,'aaaa'))
    sql = ''' UPDATE ClientList
              SET message = ? 
              WHERE id_tg_user = ?'''
    id_tg_msg = (msg, id_tg)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, id_tg_msg)
        conn.commit()
    return True


def registr (id_tg_user, nickname='', tgname='', message='', path = PATH_DEFAULLT):
    status = 'outside' #registr( '150319', 'nickname', 'tgnickname', 'там долго ещё?')
    if first_client(path) is None:
        num_id = 1
    else:
        num_id = first_client(path)[1] + count(path)
    data = '\'' + str(id_tg_user) + '\',  \'' + str(num_id) + '\',  \'' + nickname + '\', \'' + tgname + '\', \'' + status + '\', \'' + message + '\''
    try:
        insert_data('ClientList', str(data), path)
    except sqlite3.IntegrityError:
        send_message(id_tg_user, 'registration failed')
        return False
    send_message(id_tg_user,'you_last')
    return True

def i_go_home(id_tg_user, path):
    drop_client_tg_id(id_tg_user,path)
    return True