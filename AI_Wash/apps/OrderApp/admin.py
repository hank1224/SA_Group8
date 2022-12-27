from django.contrib import admin

from OrderApp.models import OrderRecord, UserData, ModeMenu, UserMode, Store, QRcode, Problem, Satisfy

class OrderRecordMain(admin.ModelAdmin):
    list_display=('sOrderID','sUserID','sSum','sPoint','sWash','sDry','sFold','sCreateTime','sFinishTime','sStoreName')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

class UserDataMain(admin.ModelAdmin):
    list_display=('sUserID','sBag')
    search_fields=('sUserID',)
    ordering=('sUserID',)

class ModeMenuMain(admin.ModelAdmin):
    list_display=('sModeName','sTime','sPrice','sPPoint')

class UserModeMain(admin.ModelAdmin):
    list_display=('sUserID','sListName','sWash','sDry','sFold')
    ordering=('sUserID',)

class StoreMain(admin.ModelAdmin):
    list_display=('sStoreID','sStoreName','sStoreAdd')
    search_fields=('sStoreID',)
    ordering=('sStoreID',)

class QRcodeMain(admin.ModelAdmin):
    list_display=('sOrderID','sCodeA','sCodeB')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

class ProblemMain(admin.ModelAdmin):
    list_display=('sOrderID','sSentTime','sDirections')
    search_fields=('sOrderID',)
    ordering=('sSentTime',)

class SatisfyMain(admin.ModelAdmin):
    list_display=('sOrderID','sServe','sRate','sSatisfy')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

    

admin.site.register(OrderRecord, OrderRecordMain)
admin.site.register(UserData, UserDataMain)
admin.site.register(ModeMenu, ModeMenuMain)
admin.site.register(UserMode, UserModeMain)
admin.site.register(Store, StoreMain)
admin.site.register(QRcode, QRcodeMain)
admin.site.register(Problem, ProblemMain)
admin.site.register(Satisfy, SatisfyMain)
