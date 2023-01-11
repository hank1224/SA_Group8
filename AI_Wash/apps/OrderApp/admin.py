from django.contrib import admin

from OrderApp.models import *

class OrderRecordMain(admin.ModelAdmin):
    list_display=('sOrderID','sUserID','sSum','sPoint','sCarbon','sWash','sDry','sFold','sCreateTime','sFinishTime','sFinish','sStoreName')
    search_fields=('sOrderID',)
    ordering=('-sCreateTime',)

class DeliveryMain(admin.ModelAdmin):
    list_display=('sOrderID','sDelivery_code','sTakeTime','sWashTime','sReciveTime','sAddress','sDelivery_Finish')
    search_fields=('sOrderID',)

class Delivery_stateMain(admin.ModelAdmin):
    list_display=('state_code','state_note','cline_display')

class UserDataMain(admin.ModelAdmin):
    list_display=('sUserID','sBag')
    search_fields=('sUserID',)
    ordering=('sUserID',)

class UserModeMain(admin.ModelAdmin):
    list_display=('sUserID','sListName','sWash','sDry','sFold')
    ordering=('sUserID',)

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

class LogindbMain(admin.ModelAdmin):
    list_display=('sState','Rstate','RuserID','RSMSid','sPhone','Raccess_code','sTime')
    search_fields=('sState',)
    ordering=('-sTime',)

    

admin.site.register(OrderRecord, OrderRecordMain)
admin.site.register(Delivery, DeliveryMain)
admin.site.register(Delivery_state, Delivery_stateMain)
admin.site.register(UserData, UserDataMain)
admin.site.register(UserMode, UserModeMain)
admin.site.register(QRcode, QRcodeMain)
admin.site.register(Problem, ProblemMain)
admin.site.register(Satisfy, SatisfyMain)
admin.site.register(Logindb, LogindbMain)