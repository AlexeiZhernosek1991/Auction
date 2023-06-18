from django.contrib import admin

from .models import *
from .utils import get_name, MyCustomError, MyCustomError2


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
            else:
                raise MyCustomError2
        else:
            if obj.lot_id.seller_id == obj.seller_id:
                id_user = get_name(str(request.user))
                name_seller = Lots.objects.get(id=obj.id)
                if name_seller.seller_id_id == id_user or str(id_user) == '1':
                    obj.seller_id = request.user
                    obj.save()
                else:
                    raise MyCustomError2
            else:
                raise MyCustomError2


admin.site.register(Lots, LotsAdmin)
admin.site.register(Bets)
admin.site.register(InfoUser)
admin.site.register(Auction_accept)
admin.site.register(User_buyer)
admin.site.register(Claim_message)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Reg_tg)
