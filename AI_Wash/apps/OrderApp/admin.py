from django.contrib import admin
from OrderApp.models import OrderRecord, UserData, Mode, ModeMenu, Common, Store, QRcode, Problem, Satisfy

class OrderRecordMain(admin.ModelAdmin):
    list_display=('sOrderID','sUserID','sSum','sPoint','sCreateTime','sFinishTime','sStoreName')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

class UserDataMain(admin.ModelAdmin):
    list_display=('sUserID','sBag','sUserMode')
    search_fields=('sUserID',)
    ordering=('sUserID',)

class ModeMain(admin.ModelAdmin):
    list_display=('sOrderID','sWash','sDry','sFold')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

class ModeMenuMain(admin.ModelAdmin):
    list_display=('sModeID','sModeName','sTime','sAmount','sPPoint')
    search_fields=('sModeID',)
    ordering=('sModeID',)

class CommonMain(admin.ModelAdmin):
    list_display=('sCommonID','sListName','sWash','sDry','sFold')
    search_fields=('sCommonID',)
    ordering=('sCommonID',)

class StoreMain(admin.ModelAdmin):
    list_display=('sStoreID','sStoreName','sStoreAdd')
    search_fields=('sStoreID',)
    ordering=('sStoreID',)

class QRcodeMain(admin.ModelAdmin):
    list_display=('sOrderID','sCodeA','sCodeB')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

class ProblemMain(admin.ModelAdmin):
    list_display=('sProblemID','sOrderID','sSentTime','sDirections')
    search_fields=('sProblemID',)
    ordering=('sProblemID',)

class SatisfyMain(admin.ModelAdmin):
    list_display=('sOrderID','sServe','sRate','sSatisfy')
    search_fields=('sOrderID',)
    ordering=('sOrderID',)

    

admin.site.register(OrderRecord, OrderRecordMain)
admin.site.register(UserData, UserDataMain)
admin.site.register(Mode, ModeMain)
admin.site.register(ModeMenu, ModeMenuMain)
admin.site.register(Common, CommonMain)
admin.site.register(Store, StoreMain)
admin.site.register(QRcode, QRcodeMain)
admin.site.register(Problem, ProblemMain)
admin.site.register(Satisfy, SatisfyMain)