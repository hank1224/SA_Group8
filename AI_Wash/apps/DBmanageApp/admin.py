from django.contrib import admin
from DBmanageApp.models import ModeMenu, Store


class ModeMenuMain(admin.ModelAdmin):
    list_display=('sModeName','sTime','sPrice','sPPoint')

class StoreMain(admin.ModelAdmin):
    list_display=('sStoreID','sStoreName','sStoreAdd')
    search_fields=('sStoreID',)
    ordering=('sStoreID',)



admin.site.register(Store, StoreMain)
admin.site.register(ModeMenu, ModeMenuMain)
# Register your models here.
