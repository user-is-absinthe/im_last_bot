import sqlite3

PATH_DEFAULLT = 'wat.db'

def con_comm(sql, value = []):
    path = PATH_DEFAULLT
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql, value)
    conn.commit()
    conn.close()
    return True

def con_get_all(sql, val =[]):
    path = PATH_DEFAULLT
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    conn.close()
    return rows

def con_get_one(sql, val =[]):
    path = PATH_DEFAULLT
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql, val)
    row = cursor.fetchone()
    conn.close()
    return row

#STG - HP, DMG, min_item, chnc_block
#INL - MP, chnc_miss, win_exp, min_item
#LCK - chnc_run, chnc_dodge, chnc_drop, win_money
#AGL - chnc_dodge, DMG, min_item, , chnc_crit

def begin_quest():
    sql0 = """create table if not exists Player
                          (id_tg_user integer PRIMARY KEY,
                          nickname text,
                          HP INTEGER,
                          MP INTEGER,
                          EXP INTEGER,
                          money INTEGER,
                          LVL INTEGER,
                          STG INTEGER,
                          INL INTEGER,
                          LCK INTEGER,
                          AGL INTEGER,
                          chnc_dodge REAL,
                          chnc_run REAL,
                          chnc_block_dmg REAL, 
                          class text,
                          review text,
                          backpack INTEGER.
                          pr_skill text,
                          ex_skill text,
                          def_skill text,
                          armor text,
                          weapon text,
                          amulet text,
                          FOREIGN KEY (baclpack) REFERENCES Backpack(id)
                          FOREIGN KEY (pr_skill) REFERENCES Skill(name_sk)
                          FOREIGN KEY (ex_skill) REFERENCES Skill(name_sk)
                          FOREIGN KEY (def_skill) REFERENCES Skill(name_sk)
                          FOREIGN KEY (armor) REFERENCES Item(name_it)
                          FOREIGN KEY (weapon) REFERENCES Item(name_it)
                          FOREIGN KEY (amulet) REFERENCES Item(name_it)
                          );
                       """
    sql1 = """create table if not exists Backpack
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          item1 text,
                          item2 text,
                          item3 text,
                          item4 text,
                          item5 text,
                          FOREIGN KEY (item1) REFERENCES Item(name_it)
                          FOREIGN KEY (item2) REFERENCES Item(name_it)
                          FOREIGN KEY (item3) REFERENCES Item(name_it)
                          FOREIGN KEY (item4) REFERENCES Item(name_it)
                          FOREIGN KEY (item5) REFERENCES Item(name_it)
                          );
                       """

    sql2 = """create table if not exists Skill
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name_sk text,
                          DMG INTEGER,
                          MP_cost INTEGER,
                          reload INTEGER, 
                          chnc_crit REAL,
                          chnc_miss REAL,
                          min_LVL INTEGER,
                          min_STG INTEGER,
                          min_INL INTEGER,
                          min_AGL INTEGER,
                          upd_dodge REAL,
                          upd_HP INTEGER,
                          upd_MP INTEGER, 
                          class text,
                          prim BLOB,
                          ext BLOB,
                          def BLOB,
                          review text);
                       """

    sql3 = """create table if not exists Item
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name_it text,
                          DMG INTEGER, 
                          chnc_crit REAL,
                          chnc_miss REAL,
                          chnc_drop REAL,                          
                          upd_block REAL,
                          upd_dodge REAL,
                          money INTEGER, 
                          upd_HP INTEGER,
                          upd_MP INTEGER, 
                          min_LVL INTEGER,
                          min_STG INTEGER,
                          min_INL INTEGER,
                          min_AGL INTEGER, 
                          class text,
                          armor BLOB,
                          weapon BLOB,
                          amulet BLOB,
                          review text);
                       """

    sql4 = """create table if not exists Event
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name_ev text,
                          EXP INTEGER,
                          money INTEGER,
                          min_LVL INTEGER,
                          v1_STG INTEGER,
                          v2_INL INTEGER,
                          v3_LCK INTEGER,
                          v4_AGL INTEGER,
                          chnc_fail REAL, 
                          review text);
                       """
    con_comm(sql4)
    con_comm(sql3)
    con_comm(sql2)
    con_comm(sql1)
    con_comm(sql0)
    return True

def sel_all(table):
    sql = 'select * from ' + str(table)
    rows = con_get_all(sql)
    return rows

def sel_atr(table, id, atr):# sel_atr('Player', 123, 'pr_skill')
    if table == 'Player':
        sql = 'select '+ str(atr)+ ' from Player WHERE id_tg_user = ' + str(id)
    else:
        sql = 'select ' + str(atr) + ' from ' + str(table) +' WHERE id = ' + str(id)
    row = con_get_one(sql)
    return row[0]

def insert_event(val):#10  insert_event( val =('test', 5, 5, 1, 1, 1, 1, 1, 0.1, 'test_event'))
    sql = '''INSERT INTO Event(name_ev, EXP, money, min_LVL, v1_STG, v2_INL, v3_LCK, v4_AGL, chnc_fail, review) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True

def insert_item(val):#19  insert_item( val =('t_item', 5, 0.05, 0.1, 0.5, 0, 0, 10, 0, 0, 1, 1, 1, 1, 't_class', 0, 1, 1, 't_weapon'))
    sql = '''INSERT INTO Item(name_it, DMG, chnc_crit, chnc_miss, chnc_drop, upd_block, upd_dodge, money, upd_HP, upd_MP, min_LVL, min_STG, min_INL, min_AGL, class, armor, weapon, amulet, review)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True

def insert_skill(val):#18 insert_skill( val =('t_skill', 10, 3, 3, 0.05, 0.1, 1, 1, 1, 1, 0, 0, 0, 't_class', 1, 0, 0, 't_atack_sk'))
    sql = '''INSERT INTO Skill(name_sk, DMG, MP_cost, reload, chnc_crit, chnc_miss, min_LVL, min_STG, min_INL, min_AGL, upd_dodge, upd_HP, upd_MP, class, prim, ext, def, review)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True


def insert_only_player(val):#22 insert_player( val =(123, 't_user', 20, 9, 0, 0, 1, 2, 3, 2, 3, 0.1, 0.15, 0.1, 't_class', 'test'))
    # sql = '''INSERT INTO Player(id_tg_user, nickname, HP, MP, EXP, money, LVL, STG, INL, LCK, AGL, chnc_dodge, chnc_run, chnc_block_dmg, class, review, pr_skill, ex_skill, def_skill, armor, weapon, amulet)
    #          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    sql = '''INSERT INTO Player(id_tg_user, nickname, HP, MP, EXP, money, LVL, STG, INL, LCK, AGL, chnc_dodge, chnc_run, chnc_block_dmg, class, review)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True

def set_skill (id_user, id_sk, sk_teg):
    sk_n = sel_atr('Skill', id_sk, 'name_sk')
    if sk_teg == 'pr':
        sk_type = 'pr_skill'
    elif sk_teg == 'ext':
        sk_type = 'ext_skill'
    elif sk_teg == 'def':
        sk_type = 'def_skill'
    else:
        return False
    sql = 'update Player set '+ sk_type +' = '+ str(sk_n) +' where id_tg_user = '+ str(id_user)


def equip_item():
    pass