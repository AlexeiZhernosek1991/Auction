from django.contrib import admin

from Bot.send import send_new_auction
# from Bot.send import send_new_auction
from .models import *
from .utils import get_name, MyCustomError, MyCustomError2, MyCustomError4


class LotsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.id == None:
            obj.seller_id = request.user
            obj.save()
        else:
            id_user = get_name(str(request.user))
            name_seller = Lots.objects.get(id=obj.id)
            if name_seller.seller_id_id == id_user or str(id_user) == '1':
                obj.seller_id = request.user
                obj.save()
            else:
                raise MyCustomError

    def delete_model(self, request, obj):
        id_user = get_name(str(request.user))
        name_seller = Lots.objects.get(id=obj.id)
        if name_seller.seller_id_id == id_user or str(id_user) == '1':
            obj.delete()
        else:
            raise MyCustomError


class AuctionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.id == None:
            print(obj.lot_id.seller_id, obj.seller_id)
            if obj.lot_id.seller_id == obj.seller_id:
                obj.seller_id = request.user
                obj.save()
                if obj.publication == True:
                    send_new_auction(-906481544,
                                     f'Продавец - {obj.seller_id} ждет подтверждения аукциона - {obj.id}. \n'
                                     f'Лот - {obj.lot_id}, стоимость - {obj.price}')
            else:
                raise MyCustomError2
        else:
            accept = Auction_accept.objects.get(auction_id=obj)
            if accept.start == True or accept.finish == True or accept.start == True:
                raise MyCustomError4
            else:
                if obj.lot_id.seller_id == obj.seller_id:
                    id_user = get_name(str(request.user))
                    name_seller = str(obj.seller_id.id)
                    name_seller_lot = str(obj.lot_id.seller_id.id)
                    if name_seller == str(id_user) and name_seller_lot == str(id_user) or str(id_user) == '1':
                        obj.seller_id = request.user
                        obj.save()
                        if obj.publication == True:
                            send_new_auction(-906481544,
                                             f'Продавец - {obj.seller_id} ждет подтверждения аукциона. \n'
                                             f'Лот - {obj.lot_id}, стоимость - {obj.price}')
                    else:
                        raise MyCustomError2
                else:
                    raise MyCustomError2


class AuctionAcceptAdmin(admin.ModelAdmin):
    list_filter = ('sold', 'accept', 'finish', 'paid_for')


admin.site.register(Lots, LotsAdmin)
admin.site.register(Bets)
admin.site.register(InfoUser)
admin.site.register(Auction_accept, AuctionAcceptAdmin)
admin.site.register(User_buyer)
admin.site.register(Claim_message)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Reg_tg)
