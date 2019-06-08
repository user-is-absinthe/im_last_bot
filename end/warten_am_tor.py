import sqlite3

PATH_DEFAULLT = 'wat.db'

def con_comm(sql):
    path = PATH_DEFAULLT
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return True

def con_get_all(sql):
    path = PATH_DEFAULLT
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

def con_get_one(sql):
    path = PATH_DEFAULLT
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row

#STG - HP, DMG, min_item
#INL - MP, chnc_miss, win_exp, min_item
#LCK - chnc_run, chnc_dodge, chnc_drop, chnc_crit
#AGL - chnc_dodge, DMG, min_item
#
#

def start_defaullt():
    sql1 = """create table if not exists Player
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
                          FOREIGN KEY (pr_skill) REFERENCES Skill(id)
                          FOREIGN KEY (ex_skill) REFERENCES Skill(id)
                          FOREIGN KEY (def_skill) REFERENCES Skill(id)
                          FOREIGN KEY (armor) REFERENCES Item(id)
                          FOREIGN KEY (weapon) REFERENCES Item(id)
                          FOREIGN KEY (amulet) REFERENCES Item(id)
                          review text);
                       """

    sql2 = """create table if not exists Skill
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name text,
                          DMG INTEGER,
                          MP_cost INTEGER,
                          reload INTEGER 
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
                          name text,
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
                          name text,
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
    return True