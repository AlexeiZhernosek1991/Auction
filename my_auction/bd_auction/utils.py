import sqlite3 as sl

con = sl.connect('D:\Пайтон\Auction\my_auction\db.sqlite3', check_same_thread=False)


def get_name(name):
    with con:
        data1 = con.execute(f'''SELECT username, id  FROM auth_user''')
        data1 = data1.fetchall()
    id_name = ''
    for x in data1:
        if name in x:
            id_name = x[1]
    return id_name


# print(type(get_name('admin')))

def get_admin():
    with con:
        data1 = con.execute(f'''SELECT bd_auction_lots.name, bd_auction_lots.price, 
                                   bd_auction_lots.date_finish, bd_auction_lots.id, bd_auction_photo.photo1, 
                                   bd_auction_photo.photo2, bd_auction_photo.photo3 
                                   FROM bd_auction_lots JOIN bd_auction_photo ON 
                                   bd_auction_lots.id = bd_auction_photo.lot_id_id
                                   WHERE bd_auction_lots.publication = 0''')
        data1 = data1.fetchall()


class MyCustomError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'MyCustomError, {0} '.format(self.message)
        else:
            return 'Вы не можете изменять или удалять этот лот'


class MyCustomError2(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'MyCustomError2, {0} '.format(self.message)
        else:
            return 'Вы не можете изменять или удалять этот Аукцион'


class MyCustomError3(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'MyCustomError3, {0} '.format(self.message)
        else:
            return 'У вас недостаточно средств чтоб объявить аукцион'


class MyCustomError4(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'MyCustomError4, {0} '.format(self.message)
        else:
            return 'Данный аукцион нельзя изменять.\n' \
                   'Отменить аукцион можно в кабинете ТГ БОТА'


class MyCustomError5(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'MyCustomError5, {0} '.format(self.message)
        else:
            return 'У вас недостаточно средств для отмены аукциона'
