import sqlite3
from numpy import random as np


PATH_DEFAULLT = 'wat.db'
PATH_JPG = '\wat_img' #+ type+'_'+name+'.jpg'

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
                          chnc_miss_p REAL,
                          chnc_crit_p REAL,
                          chnc_drop_p REAL, 
                          chnc_dodge REAL,
                          chnc_run REAL,
                          chnc_block_dmg REAL,
                          blk_dmg REAL, 
                          class text,
                          review text,
                          backpack INTEGER,
                          pr_skill text,
                          ex_skill text,
                          def_skill text,
                          armor text,
                          weapon text,
                          amulet text,
                          FOREIGN KEY (backpack) REFERENCES Backpack(id)
                          FOREIGN KEY (pr_skill) REFERENCES Skill(name_sk)
                          FOREIGN KEY (ex_skill) REFERENCES Skill(name_sk)
                          FOREIGN KEY (def_skill) REFERENCES Skill(name_sk)
                          FOREIGN KEY (armor) REFERENCES Item(name_it)
                          FOREIGN KEY (weapon) REFERENCES Item(name_it)
                          FOREIGN KEY (amulet) REFERENCES Item(name_it)
                          );
                       """

    sql1 = """create table if not exists Backpack
                          (id INTEGER PRIMARY KEY,
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
                          BLK REAL, 
                          chnc_crit REAL,
                          chnc_miss REAL,
                          chnc_drop REAL,                          
                          upd_ch_block REAL,
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

def get_img_name(type, name):
    img_name = PATH_JPG +str(type) + '_' + str(name) + '.jpg'
    return img_name

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

def sel_sk_id(sk_name):
    sql = 'select id from Skill WHERE  name_sk = ?'
    row = con_get_one(sql, [sk_name])
    return int(row[0])

#по неясной причине вместо имен предметов в базу идут их айди
def sel_it_id(it_name):
    sql = 'select id from Item WHERE  name_it = ?'
    row = con_get_one(sql, [it_name])
    return int(row[0])

def upd_player_stat(id_user, atr, val):#upd_player_stat(123, ('HP', 'MP'), (10,15))
    i=0
    for a in atr:
        sql = 'update Player set ' + str(a) + ' = ? where id_tg_user = ?'
        con_comm(sql, (val[i],id_user))
        i=i+1
    return True

def insert_event(val):#10  insert_event( val =('test', 5, 5, 1, 1, 1, 1, 1, 0.1, 'test_event'))
    sql = '''INSERT INTO Event(name_ev, EXP, money, min_LVL, v1_STG, v2_INL, v3_LCK, v4_AGL, chnc_fail, review) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True

def insert_item(val):
         #insert_item( val =('t_apok', 5, 0, 0.1, 0.05, 0.6, 0.1, 0, 10, 0, 0, 1, 1, 1, 1, 't_class', 0, 1, 0, 't_weapon'))
          #insert_item( val=('ar_itm', 0, 0.7, 0, 0, 0.7, 0.5, 0.05, 5, 3, 4, 1, 1, 1, 1, 't_class', 1, 0, 0, 't_armor'))
         #insert_item( val =('statue', 3, 0, 0, 0, 0.3, 0.3, 0.05, 15, -1, 5, 1, 1, 1, 1, 't_class', 0, 0, 1, 't_amulet'))
    sql = '''INSERT INTO Item(name_it, DMG, BLK, chnc_crit, chnc_miss, chnc_drop, upd_ch_block, upd_dodge, money, upd_HP, upd_MP, min_LVL, min_STG, min_INL, min_AGL, class, armor, weapon, amulet, review)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True

def insert_skill(val):
    #insert_skill( val =('t_skill', 10, 3, 3, 0.05, 0.1, 1, 1, 1, 1, 0, 0, 0, 't_class', 1, 0, 0, 't_atack_sk'))
    #insert_skill(val=('t_def_sk', 0, 4, 3, 0, 0, 1, 1, 1, 1, 0.1, 5, 5, 't_class', 0, 0, 1, 't_def_sk'))
    sql = '''INSERT INTO Skill(name_sk, DMG, MP_cost, reload, chnc_crit, chnc_miss, min_LVL, min_STG, min_INL, min_AGL, upd_dodge, upd_HP, upd_MP, class, prim, ext, def, review)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    con_comm(sql,val)
    return True

#STG - HP, DMG, min_item, chnc_block
#INL - MP, chnc_miss, win_exp, min_item
#LCK - chnc_run, chnc_dodge, chnc_drop, win_money
#AGL - chnc_dodge, DMG, min_item, , chnc_crit

def upd_lvl(id_user):
    exp = sel_atr('Player', id_user, 'EXP')
    lvl = sel_atr('Player', id_user, 'LVL')
    exp_lvl = 1+ int(10*lvl*(1 + 0.25* (lvl-1)))
    while exp > exp_lvl:
        lvl = lvl +1
        exp_lvl = 1 + int(10 * lvl * (1 + 0.25 * (lvl - 1)))
    upd_player_stat(id_user, ['LVL'], str(lvl))
    return True

def gen_stat(LVL, STG, INL):
    HP = 5 + LVL*3 + STG*3
    MP = 5 + LVL*3 + INL*3
    return (HP, MP)

def gen_chnc(LVL, STG, INL, LCK, AGL):#генерация вторичных характеристик из первичных
    LVL = int (LVL)
    STG = int (STG)
    INL = int (INL)
    LCK = int (LCK)
    AGL = int (AGL)
    c_dodge = 0.025 + 0.01*LVL + 0.025*(AGL+LCK)
    if c_dodge > 0.9: c_dodge = 0.9
    c_run = 0.25-LVL*0.05 + LCK*0.1
    if c_run > 0.9: c_run = 0.9
    c_drop = 0.35 + 0.05*LVL + 0.1*LCK
    if c_drop > 0.9: c_drop = 0.9
    c_block_dmg = 0.25 + 0.05*LVL + STG*0.125
    if c_block_dmg > 0.9: c_block_dmg = 0.9
    c_crit = 0.01 + 0.005*LVL + 0.05*AGL
    if c_crit > 0.9: c_crit = 0.9
    c_miss = 0.8 - LVL*0.15 - INL*0.2-(LCK+AGL)*0.05
    if c_miss > 0.7: c_miss = 0.7
    if c_miss < 0.05: c_miss = 0.05
    blk_dmg = 0.15 + 0.01*(LVL+STG+INL+LCK+AGL)
    if blk_dmg > 0.9: blk_dmg = 0.9
    return (c_miss, c_crit, c_drop, c_dodge, c_run, c_block_dmg, blk_dmg)


def insert_only_player(val):#вставка записи по основным статистикам, вторичные генерируются, ссылки на прдметы и скиллы указываются отдельно
    # insert_only_player( val = id_tg_user, nickname, EXP, money, LVL, STG, INL, LCK, AGL, class, review
    # insert_only_player( val =(111, 'palladin', 0, 0, 1, 4, 2, 1, 2, 't_class', 'test'))
    # insert_only_player( val =(123, 't_user', 0, 0, 1, 2, 3, 2, 2, 't_class', 'test'))
    # insert_only_player( val =(100, 'toster', 0, 0, 1, 3, 1, 3, 2, 't_class', 'tester'))
    # sql = '''INSERT INTO Player(id_tg_user, nickname, HP, MP, EXP, money, LVL, STG, INL, LCK, AGL, chnc_dodge, chnc_run, chnc_block_dmg, class, review, backpack, pr_skill, ex_skill, def_skill, armor, weapon, amulet)
    #          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    sql = '''INSERT INTO Backpack(id) VALUES (''' + str(val[0]) + ')'
    try:
        con_comm(sql)
    except sqlite3.IntegrityError:
#TODO: сделать уведомление и возможность пересоздания
        print('your backpack is already exist')

    (chnc_miss_p, chnc_crit_p, chnc_drop_p, chnc_dodge, chnc_run, chnc_block_dmg, blk_dmg) = gen_chnc(val[4],val[5],val[6],val[7], val[8])
    (HP, MP) = gen_stat(val[4],val[5],val[6])
    sql = '''INSERT INTO Player(id_tg_user, nickname, HP, MP, EXP, money, LVL, STG, INL, LCK, AGL,
             chnc_miss_p, chnc_crit_p, chnc_drop_p, chnc_dodge, chnc_run, chnc_block_dmg, blk_dmg, class, review, backpack) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    value = (val[0],val[1],HP, MP,val[2],val[3],val[4],val[5],val[6],val[7],val[8],
             chnc_miss_p, chnc_crit_p, chnc_drop_p, chnc_dodge, chnc_run, chnc_block_dmg, blk_dmg,
             val[9],val[10], val[0])
    try:
        con_comm(sql,value)
    except sqlite3.IntegrityError:
        print('you is already exist')
    return True

def drop_all(table):
    sql = 'DROP TABLE '+ str(table)
    con_comm(sql)
    return True

def drop_str(table, id_str):
    sql = 'DELETE FROM ' + str(table) +' WHERE id = ' + str(id_str)
    con_comm(sql)
    return True

def drop_player(id_user):
    drop_str('Backpack', id_user)
    sql = 'DELETE FROM Player WHERE id_tg_user = ?'
    con_comm(sql,[str(id_user)])
    return True

def set_skill (id_user, id_sk, sk_teg): #экипировка доступного скилла в один из слотов
    # set_skill(123, 1, 'prim')
    sk_n = sel_atr('Skill', id_sk, 'name_sk')

    if sk_teg == 'prim':
        sk_type = 'pr_skill'
    elif sk_teg == 'ext':
        sk_type = 'ext_skill'
    elif sk_teg == 'def':
        sk_type = 'def_skill'
    else:
        return False

# TODO: сделать уведомлениz
    if sel_atr('Skill', id_sk, 'min_LVL') > sel_atr('Player', id_user, 'LVL'):
        print('need more lvl')
        return False

    if sel_atr('Skill', id_sk, 'min_STG') > sel_atr('Player', id_user, 'STG'):
        print('need more stg')
        return False

    if sel_atr('Skill', id_sk, 'min_INL') > sel_atr('Player', id_user, 'INL'):
        print('need more inl')
        return False

    if sel_atr('Skill', id_sk, 'min_AGL') > sel_atr('Player', id_user, 'AGL'):
        print('need more agl')
        return False

    if sel_atr('Skill', id_sk, str(sk_teg)) == 0:
        print('change skill_type')
        return False

    prev_sk = sel_atr('Player', id_user, sk_type)
    if prev_sk is not None:
        pr_sk_id = sel_sk_id(prev_sk)
        HP_sk = sel_atr('Skill', pr_sk_id, 'upd_HP')
        MP_sk = sel_atr('Skill', pr_sk_id, 'upd_MP')
        c_d_sk = sel_atr('Skill', pr_sk_id, 'upd_dodge')
    else:
        HP_sk = 0
        MP_sk =0
        c_d_sk = 0

    sql = 'update Player set '+ sk_type +' = \''+ str(sk_n) +'\' where id_tg_user = '+ str(id_user)
    con_comm(sql)
    print('Skill ', sk_n, 'equip')


    p_dodge = sel_atr('Skill', id_sk, 'upd_dodge') + sel_atr('Player', id_user, 'chnc_dodge') - c_d_sk
    if p_dodge> 0.9:
        p_dodge = 0.9
    atr_sk = ('HP', 'MP', 'chnc_dodge')
    val_sk = (sel_atr('Skill', id_sk, 'upd_HP')+sel_atr('Player', id_user, 'HP') - HP_sk,
              sel_atr('Skill', id_sk, 'upd_MP')+sel_atr('Player', id_user, 'MP') - MP_sk,
              p_dodge
              )

    upd_player_stat(id_user, atr_sk, val_sk)
    return True

def put_in_backpack(it_id, id_user):
    if sel_atr('Backpack', id_user, 'item5') is not None:
        print('Backpack full')
        return False
    i=5
    if sel_atr('Backpack', id_user, 'item4') is None:
        i=4
        if sel_atr('Backpack', id_user, 'item3') is None:
            i=3
            if sel_atr('Backpack', id_user, 'item2') is None:
                i=2
                if sel_atr('Backpack', id_user, 'item1') is None:
                    i=1
    sql = 'update Backpack set item'+str(i)+'= '+str(it_id)+' where id = '+str(id_user)
    try:
        con_comm(sql)
    except sqlite3.OperationalError:
        print('NoneType insert')
    return i
#TODO:проблемы со вставкой
def put_out_backpack(it_num, id_user):
    sql = 'select * from Backpack WHERE id = ?'
    str_l = con_get_one(sql, [id_user])
    list = []
    for i in range(1,6):
        if i != it_num:
            list.append(str_l[i])
        else:
            id_it = str_l[i]
    drop_str('Backpack', id_user)
    sql = '''INSERT INTO Backpack(id) VALUES (''' + str(id_user) + ')'
    con_comm(sql)
    for i in range(0,4):
        try:
            put_in_backpack(list[i],id_user)
        except TypeError:
            print('NoneType insert')
    return id_it

def item_in_pocket(it_num, id_user):
    sql = 'select * from Backpack WHERE id = ?'
    str_l = con_get_one(sql, [id_user])
    id_it = str_l[it_num]
    return id_it

def found_item(id_user):# подбор лута
    try:
        sel_atr('Backpack', id_user, 'item5')
    except TypeError:
        print("NoneType insert. Check id")
        return False
    if sel_atr('Backpack', id_user, 'item5') is not None:
        print('Backpack full')
        return False
    p_drop = sel_atr('Player', id_user, 'chnc_drop_p')
    p_item_drop = np.rand()
    print(p_drop, p_item_drop)
    if p_drop > p_item_drop:#выпадет ли что-то с моба
        sql = 'select id, chnc_drop from Item'
        it_list = con_get_all(sql)
        n = len(it_list)
        p = []
        id_it = []
        for i in range(0, n):
            p.append(it_list[i][1])
            id_it.append(it_list[i][0])
        S_=1/sum(p)
        for i in range(0, n):
            p[i] = p[i] * S_
        new_item_id = int(np.choice(id_it,1,p)[0])#что именно выпадет
        it_name = sel_atr('Item', new_item_id, 'name_it')
        print('Found ', it_name)
        i = put_in_backpack(new_item_id, id_user) #предмет отправляется в рюкзак
        print(it_name,' is in the pocket ',i)
        return True
    else:
        print('New items not found')
        return False
    pass

# TODO: Не забыть об изменениях характеристик героя
def equip_item(id_user, it_n, it_type):
    it_id = item_in_pocket(it_n, id_user)
    if it_id is None:
        print('Pocket is empty')
        return False
    it_name = sel_atr('Item',it_id, 'name_it')
    if sel_atr('Item', it_id, str(it_type)) == 0:
        print('change item_type ')
        return False

    if sel_atr('Item', it_id, 'min_LVL') > sel_atr('Player', id_user, 'LVL'):
        print('need more lvl')
        return False

    if sel_atr('Item', it_id, 'min_STG') > sel_atr('Player', id_user, 'STG'):
        print('need more stg')
        return False

    if sel_atr('Item', it_id, 'min_INL') > sel_atr('Player', id_user, 'INL'):
        print('need more inl')
        return False

    if sel_atr('Item', it_id, 'min_AGL') > sel_atr('Player', id_user, 'AGL'):
        print('need more agl')
        return False

    prev_it = sel_atr('Player', id_user, it_type)
    if prev_it is not None:
        pr_id = sel_it_id(prev_it)
        HP_it = sel_atr('Item', pr_id, 'upd_HP')
        MP_it = sel_atr('Item', pr_id, 'upd_MP')
        c_dod = sel_atr('Item', pr_id, 'upd_dodge')
        c_blk = sel_atr('Item', pr_id, 'upd_ch_block')
    else:
        HP_it = 0
        MP_it =0
        c_dod = 0
        c_blk = 0

    sql = 'update Player set ' + it_type + ' = \'' + str(it_name) + '\' where id_tg_user = ' + str(id_user)
    con_comm(sql)
    print('Item ', it_name, 'equip')
    # устраняем влияние прошлого предмета
    p_dodge = sel_atr('Item', it_id, 'upd_dodge') + sel_atr('Player', id_user, 'chnc_dodge') - c_dod
    if p_dodge > 0.9:
        p_dodge = 0.9

    p_blk = sel_atr('Item', it_id, 'upd_ch_block') + sel_atr('Player', id_user, 'chnc_block_dmg') - c_blk
    if p_blk > 0.9:
        p_blk = 0.9

    blk_it_n=sel_atr('Item', it_id, 'BLK')
    blk_pl= gen_chnc(sel_atr('Player', id_user, 'LVL'),
                     sel_atr('Player', id_user, 'STG'),
                     sel_atr('Player', id_user, 'INL'),
                     sel_atr('Player', id_user, 'LCK'),
                     sel_atr('Player', id_user, 'AGL')
                     )[-1]
    BLK = max(blk_pl, blk_it_n) # блок считается как максимум от нового прдмета и стат игрока без предметов
    atr_sk = ('HP', 'MP', 'chnc_dodge', 'chnc_block_dmg', 'blk_dmg')
    val_sk = (sel_atr('Item', it_id, 'upd_HP') + sel_atr('Player', id_user, 'HP') - HP_it,
              sel_atr('Item', it_id, 'upd_MP') + sel_atr('Player', id_user, 'MP') - MP_it,
              p_dodge,
              p_blk,
              BLK
              )

    upd_player_stat(id_user, atr_sk, val_sk)
    put_out_backpack(it_n, id_user)
    return True