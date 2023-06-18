import sqlite3 as sl

con = sl.connect('D:\Пайтон\Auction\my_auction\db.sqlite3', check_same_thread=False)


#
#
# def registration(dict_):
#     # print(dict_)
#     #  функция принимает в качестве аргумента словарь со значениями, возвращает TRUE при успехе или ошибку при ошибке
#     """
#     :param Словарь:
#     :return: таблицу User c заполненными данными
#     vk_id TEXT,
#     tg_id TEXT);
#     """
#     try:
#         sql_insert = f"INSERT INTO auth_user (username, password,tg_id, is_superuser ) values(?,?,?,?)"
#         with con:
#             con.execute(sql_insert, (dict_["name"], dict_["password"], dict_["tg_id"], '0'))
#     except Exception as e:
#         print('не сработало')
#         print(e)
#
# registration({"tg_id": 515215,"name": "KAtya","password":"mmaa1234"})

def get_auctions():
    with con:
        data1 = con.execute(f'''SELECT bd_auction_lots.name, bd_auction_lots.price, 
                                   bd_auction_lots.date_finish, bd_auction_lots.id, bd_auction_lots.photo1, 
                                   bd_auction_lots.photo2, bd_auction_lots.photo3 
                                   FROM bd_auction_lots
                                   WHERE bd_auction_lots.publication = 0''')
        data1 = data1.fetchall()
    # print(data1)
    list_dict_lots = []
    for i in data1:
        dict_lot = {}
        dict_lot['name'] = i[0]
        dict_lot['price'] = i[1]
        dict_lot['time_finish'] = i[2]
        dict_lot['id'] = i[3]
        list_photo = []
        for photo in list(i[4:]):
            if photo != '':
                list_photo.append(photo)
        dict_lot['photo'] = list_photo
        list_dict_lots.append(dict_lot)
    print(list_dict_lots)
    return list_dict_lots


# get_lots()

def reg_user_byers(tg_id):
    sql_insert = f"INSERT INTO bd_auction_user_buyer (tg_id, strike_count) values(?,?)"
    with con:
        con.execute(sql_insert, (str(tg_id), 0))
    return True


# reg_user_byers(1)

def get_user_byers(tg_id):
    with con:
        data1 = con.execute(f'''SELECT * FROM bd_auction_user_buyer WHERE tg_id = {tg_id}''')
        data1 = data1.fetchall()
        if len(data1) > 0:
            return True
        else:
            return False


# print(get_user_byers(113966137))


# def is_publish(id_lot):
#     com = f"UPDATE bd_auction_lots SET publication = ? WHERE id = ?"
#     with con:
#         con.execute(com, ('1', id_lot))


# is_publish('1')

def get_lot(id_lot):
    with con:
        data1 = con.execute(f'''SELECT bd_auction_lots.name, bd_auction_lots.price, 
                                      bd_auction_lots.date_finish, bd_auction_lots.id, bd_auction_lots.photo1, 
                                      bd_auction_lots.photo2, bd_auction_lots.photo3 
                                      FROM bd_auction_lots
                                      WHERE bd_auction_lots.id = {id_lot}''')
        data1 = data1.fetchall()
    i = data1[0]
    dict_lot = {}
    dict_lot['name'] = i[0]
    dict_lot['price'] = i[1]
    dict_lot['time_finish'] = i[2]
    dict_lot['id'] = i[3]
    list_photo = []
    for x in list(i[4:]):
        if x != '':
            list_photo.append(x)
    dict_lot['photo'] = list_photo
    print(dict_lot)
    return dict_lot


# get_lot('1')

def get_name(name):
    with con:
        data1 = con.execute(f'''SELECT username, id  FROM auth_user''')
        data1 = data1.fetchall()
        print(data1)
    id_name = ''
    for x in data1:
        if name in x:
            id_name = x[1]
    print(id_name)


# get_name('jana')

def reg_seller_tg(tg_id, username):
    sql_insert = f"INSERT INTO bd_auction_reg_tg (username, id_tg) values(?,?)"
    with con:
        con.execute(sql_insert, ('@' + username, str(tg_id)))
    return True


def get_seller_tg(id_tg):
    with con:
        data1 = con.execute(f'''SELECT username, id_tg  FROM bd_auction_reg_tg WHERE id_tg = {id_tg}''')
        data1 = data1.fetchall()
        print(data1)
    if len(data1) > 0:
        return True
    else:
        return False


# print(get_seller_tg(113966137))

def tg_id_in_bdinfouser(id_tg):
    with con:
        data1 = con.execute(f'''SELECT username_tg,tg_id  FROM bd_auction_infouser WHERE tg_id = {id_tg}''')
        data1 = data1.fetchall()
        print(data1)
    if len(data1) > 0:
        return True
    else:
        return False


print(tg_id_in_bdinfouser(1139661376))
