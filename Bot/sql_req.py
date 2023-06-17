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

def get_lots():
    with con:
        data1 = con.execute(f'''SELECT bd_auction_lots.name, bd_auction_lots.price, 
                                   bd_auction_lots.date_finish, bd_auction_lots.id, bd_auction_photo.photo1, 
                                   bd_auction_photo.photo2, bd_auction_photo.photo3 
                                   FROM bd_auction_lots JOIN bd_auction_photo ON 
                                   bd_auction_lots.id = bd_auction_photo.lot_id_id
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
        dict_lot['photo'] = list(i[4:])
        list_dict_lots.append(dict_lot)
    print(list_dict_lots)
    return list_dict_lots


# get_lots()


def is_publish(id_lot):
    com = f"UPDATE bd_auction_lots SET publication = ? WHERE id = ?"
    with con:
        con.execute(com, ('1', id_lot))


# is_publish('1')

def get_lot(id_lot):
    with con:
        data1 = con.execute(f'''SELECT bd_auction_lots.name, bd_auction_lots.price, 
                                      bd_auction_lots.date_finish, bd_auction_lots.id, bd_auction_photo.photo1, 
                                      bd_auction_photo.photo2, bd_auction_photo.photo3 
                                      FROM bd_auction_lots JOIN bd_auction_photo ON 
                                      bd_auction_lots.id = bd_auction_photo.lot_id_id
                                      WHERE bd_auction_lots.id = {id_lot}''')
        data1 = data1.fetchall()
    i = data1[0]
    dict_lot = {}
    dict_lot['name'] = i[0]
    dict_lot['price'] = i[1]
    dict_lot['time_finish'] = i[2]
    dict_lot['id'] = i[3]
    dict_lot['photo'] = list(i[4:])
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
