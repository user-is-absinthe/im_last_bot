import sqlite3


# path_to_db = ":memory:"
path_to_db = "test.db"

connector = sqlite3.connect(path_to_db)
my_cursor = connector.cursor()

sql_q = """create table if not exists ClientList
                      (id_tg_user integer PRIMARY KEY,
                      me_num int,
                      nickname text,
                      tgname text,
                      status text,
                      message text);
                   """
my_cursor.execute(sql_q)
connector.commit()

# sql_q = '''insert into ClientList values (?, ?, ?, ?, ?, ?)'''
# my_cursor.execute(sql_q, (1, 2, 'vasa', '@vasa', 'status_old', 'message_old'))
# connector.commit()

# sql_q = """update ClientList set status = 'status_n', message = 'message_n' where ClientList.id_tg_user = 1"""
# my_cursor.execute(sql_q)
# connector.commit()

sql = ''' UPDATE ClientList
              SET message = ? 
              WHERE id_tg_user = ?'''
conn = sqlite3.connect(path_to_db)
cursor = conn.cursor()
id_tg_msg = ('message_another', 1)
cursor.execute(sql, id_tg_msg)
conn.commit()
conn.close()
