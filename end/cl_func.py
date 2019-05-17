import sqlite3

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
                      me_num int,
                      nickname text,
                      tgname text,
                      status text,
                      message text);
                   """
    connector(sql, path)
    sql = """create table if not exists Banner
                      (id integer PRIMARY KEY,
                      firma text,
                      text_banner text,
                      period int);
                   """
    connector(sql, path)
    return True

# TODO: Оповещение уже в тг-части. Триггер для Плотвы
def send_message(id_tg_user, message):
    pass

def insert_data (table_name, data, path):
    sql = 'insert into ' + str(table_name) + ' values ( ' + str(data) + ' )'
    connector(sql,path)

def select_cl(me_num, path):
    sql = "select * from ClientList where me_num == "+ str(me_num)
    # cursor.execute(sql)
    row = connector(sql,path)#cursor.fetchone()
    return row

def select_cl_id_tg(id_tg, path):
    sql = "select * from ClientList where id_tg_user == "+ str(id_tg)
    # cursor.execute(sql)
    # row = cursor.fetchone()
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


def drop_client_tg_id (id_tg, path):
    send_message(id_tg, 'you_go_away')
    sql = 'delete from ClientList where id_tg_str = ' + str(id_tg)
    connector(sql,path)

def drop_all_cl (path= PATH_DEFAULLT): # очистка очереди
    for i in range (0,count()-1):
        id_tg_user = all_client()[i][0]
        send_message(id_tg_user, 'go_home')
    sql = 'delete from ClientList'
    connector(sql,path)


def prev_client (me_num, path = PATH_DEFAULLT):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        sql = "select * from ClientList where me_num == "+ str(me_num-1)
        cursor.execute(sql)
        row = cursor.fetchall()
        if len(row) == 0 and count() > 0:
            i = 2
            while len(row) == 0:
                sql = "select * from ClientList where me_num == " + str(me_num - i)
                cursor.execute(sql)
                row = cursor.fetchall()
                i = i +1
    return row

def count_before(me_num, path = PATH_DEFAULLT):
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        sql = "select count(*) from ClientList where me_num < "+ str(me_num)
        cursor.execute(sql)
        count_l = cursor.fetchall()
        count_l = count_l[0][0]

    return count_l


def first_client (path):# первый
    sql = 'select * from ClientList' # where id = 1
    row = connector(sql,path)
    # cursor.execute(sql)
    # row = cursor.fetchone()
    return row

def im_in(id_tg_user, path):#зашел на сдвчу
    sql = '''update ClientList set status = 'inside' where id_tg_user = ''' + str(id_tg_user)
    # cursor.execute(sql)
    # conn.commit()
    connector(sql,path)
    send_message(id_tg_user, 'you_come_in')
    pass

def im_out(id_tg_user, path= PATH_DEFAULLT):# вышел, запускайте следующего
    drop_client_tg_id(id_tg_user)
    send_message(str(first_client ()[0]), 'you_first')

def upd_message(id_tg,msg, path):
    sql = 'update ClientList set message ='+ str(msg) +'where id_tg_user = ' + str(id_tg)
    connector(sql,path)


# TODO: update username (by id)

def registr (id_tg_user, nickname='', tgname='', message='', path= PATH_DEFAULLT):
    status = 'outside' #registr( '150319', 'nickname', 'tgnickname', 'там долго ещё?')
    if count(path) > 0:
        me_num = str(all_client()[-1][0]+ 1)
    else:
        me_num = 1
    data = '\'' + str(id_tg_user) + '\', \'' + str(me_num) + '\', \'' + nickname + '\', \'' + tgname + '\', \'' + status + '\', \'' + message + '\''
    insert_data('ClientList', str(data), path)
    send_message(id_tg_user,'you_last')
    return True

