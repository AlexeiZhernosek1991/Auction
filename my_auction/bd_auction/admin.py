from django.contrib import admin

from .models import *
from .utils import get_name, MyCustomError


class LotsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.id == None:
            obj.seller_id = request.user
            obj.save()
            # accept = Lots_accept()
            # lot_id =
            # accept.lot_id = lot_id
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


admin.site.register(Lots, LotsAdmin)
admin.site.register(Bets)
admin.site.register(InfoUser)
admin.site.register(Lots_accept)
admin.site.register(User_buyer)
admin.site.register(Claim_message)
