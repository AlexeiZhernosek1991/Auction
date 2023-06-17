from django.contrib import admin

from .models import *
from .utils import get_name, MyCustomError


class LotsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(obj.id)
        if obj.id == None:
            if getattr(obj, 'seller_id', None) is None:
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


admin.site.register(Lots, LotsAdmin)
admin.site.register(Bets)
