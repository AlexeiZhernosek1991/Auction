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
    r""":return начало, конец,
    @usename, название, описание,
    фото1, фото2, фото3, файл,
    текущую стоимость, id bd_auction_auction_accept"""
    with con:
        data1 = con.execute(f'''SELECT bd_auction_auction.date_start, bd_auction_auction.date_finish,
                            bd_auction_infouser.username_tg, bd_auction_lots.name, bd_auction_lots.description,
                            bd_auction_lots.photo1, bd_auction_lots.photo2, bd_auction_lots.photo3, 
                            bd_auction_lots.file_rar, bd_auction_auction_accept.price_finish, 
                            bd_auction_auction_accept.id
                            FROM bd_auction_auction JOIN bd_auction_auction_accept ON 
                            bd_auction_auction.id = bd_auction_auction_accept.auction_id_id
                            JOIN bd_auction_lots ON 
                            bd_auction_auction.lot_id_id = bd_auction_lots.id
                            JOIN bd_auction_infouser ON 
                            bd_auction_auction.seller_id_id = bd_auction_infouser.user_id_id
                            WHERE bd_auction_auction_accept.accept = 1 
                            AND bd_auction_auction_accept.start = 0''')
        data1 = data1.fetchall()
        list_dict = []
        for auc in data1:
            auc_dict = {'stat_time': auc[0],
                        'finish_time': auc[1],
                        'username': auc[2],
                        'name': auc[3],
                        'desc': auc[4],
                        'file': auc[8],
                        'price': auc[9],
                        'id_accept': auc[10]
                        }
            list_photo = []
            for f in list(auc)[5:8]:
                if len(f) > 1:
                    list_photo.append(f)
                else:
                    pass
            auc_dict['photo'] = list_photo
            list_dict.append(auc_dict)
        return list_dict


# print(get_auctions())

def start_true(auction):
    com = f"UPDATE bd_auction_auction_accept SET start = ? WHERE id = {auction}"
    with con:
        con.execute(com, ('1',))


# start_true(2)


def reg_user_byers(tg_id):
    sql_insert = f"INSERT INTO bd_auction_user_buyer (tg_id) values(?)"
    with con:
        con.execute(sql_insert, (str(tg_id),))
    return True


# reg_user_byers(1139661376)

def get_user_byers(tg_id):
    with con:
        data1 = con.execute(f'''SELECT * FROM bd_auction_user_buyer WHERE tg_id = {tg_id}''')
        data1 = data1.fetchall()
        if len(data1) > 0:
            return True
        else:
            return False


def user_byers(tg_id):
    with con:
        data1 = con.execute(f'''SELECT bd_auction_user_buyer.id FROM bd_auction_user_buyer WHERE tg_id = {tg_id}''')
        data1 = data1.fetchall()
        return list(data1[0])[0]


# print(user_byers(1139661376))


# def is_publish(id_lot):
#     com = f"UPDATE bd_auction_lots SET publication = ? WHERE id = ?"
#     with con:
#         con.execute(com, ('1', id_lot))


# is_publish('1')

def get_auc(id_lot):
    data1 = con.execute(f'''SELECT bd_auction_auction.date_start, bd_auction_auction.date_finish,
                                bd_auction_infouser.username_tg, bd_auction_lots.name, bd_auction_lots.description,
                                bd_auction_lots.photo1, bd_auction_lots.photo2, bd_auction_lots.photo3, 
                                bd_auction_lots.file_rar, bd_auction_auction_accept.price_finish, 
                                bd_auction_auction_accept.id
                                FROM bd_auction_auction JOIN bd_auction_auction_accept ON 
                                bd_auction_auction.id = bd_auction_auction_accept.auction_id_id
                                JOIN bd_auction_lots ON 
                                bd_auction_auction.lot_id_id = bd_auction_lots.id
                                JOIN bd_auction_infouser ON 
                                bd_auction_auction.seller_id_id = bd_auction_infouser.user_id_id
                                WHERE bd_auction_auction_accept.id = {id_lot}''')
    data1 = data1.fetchall()
    auc_dict = {}
    for auc in data1:
        auc_dict = {'stat_time': auc[0],
                    'finish_time': auc[1],
                    'username': auc[2],
                    'name': auc[3],
                    'desc': auc[4],
                    'file': auc[8],
                    'price': auc[9],
                    'id_accept': auc[10]
                    }
        list_photo = []
        for f in list(auc)[5:8]:
            if len(f) > 1:
                list_photo.append(f)
            else:
                pass
        auc_dict['photo'] = list_photo
    return auc_dict


# print(get_auc('3'))

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


def get_user_buyer(id):
    with con:
        data1 = con.execute(f'''SELECT wallet, good_buy  FROM bd_auction_user_buyer WHERE bd_auction_user_buyer.tg_id = {id}''')
        data1 = data1.fetchall()
        print(data1)
    if len(data1) > 0:
        return True
    else:
        return False
get_user_buyer(1139661376)
# print(tg_id_in_bdinfouser(1139661376))
