from django.db import models
from datetime import datetime
from uuid import uuid4
def wStateUUID():
    return "wState-"+str(uuid4())
def sOrderIDUUID():
    return "Order-"+str(uuid4())

class OrderRecord(models.Model):
    sOrderID=models.CharField(max_length=42, primary_key=True ,default=sOrderIDUUID)
    sUserID=models.CharField(max_length=43, null=False)
    sSum=models.FloatField(blank=False, null=False)
    sPoint=models.FloatField(blank=False, null=False)
    sCarbon=models.FloatField(blank=False, null=False)
    sWash=models.CharField(max_length=5, null=False)
    sDry=models.CharField(max_length=4, null=False)
    sFold=models.CharField(max_length=5, null=False)
    sOrderType=models.CharField(max_length=6, null=False)
    sCreateTime=models.DateTimeField(auto_now_add=True)
    sFinishTime=models.DateTimeField(blank=False, null=True, default=None)
    sTakeTime=models.CharField(max_length=20, null=True, default=None)
    sDelivery=models.BooleanField(null=False, default=False)
    sStoreName=models.CharField(max_length=10,blank=False, null=False)
    
    class Meta:
        verbose_name = u"訂單記錄"
        verbose_name_plural = verbose_name


class Delivery(models.Model):
    sOrderID=models.ForeignKey("OrderRecord", on_delete=models.RESTRICT)
    sDelivery_code=models.ForeignKey("delivery_state", on_delete=models.RESTRICT)
    sAddress=models.CharField(max_length=100, null=False)
    sTakeTime=models.DateTimeField(null=False)
    sReciveTime=models.DateTimeField(null=False)
    sDelivery_Finish=models.BooleanField(default=False)

    class Meta:
        verbose_name = u"外送訂單"
        verbose_name_plural = verbose_name

class Delivery_state(models.Model):
    state_code=models.IntegerField(primary_key=True, null=False)
    state_note=models.CharField(max_length=20)
    cline_display=models.CharField(max_length=20)

    class Meta:
        verbose_name = u"外送單代碼"
        verbose_name_plural = verbose_name

class UserData(models.Model):
    sUserID=models.CharField(max_length=43, null=False, primary_key=True)
    sBag=models.PositiveIntegerField(blank=False ,null=False, default=0)

    class Meta:
        verbose_name = u"顧客資料"
        verbose_name_plural = verbose_name

    #def __str__(self):
        #return self.sUserID
    #讓object預設回傳


class UserMode(models.Model):
    sUserID=models.ForeignKey('UserData', on_delete=models.CASCADE)
    sListName=models.CharField(max_length=20, blank=False, null=False)
    sWash=models.CharField(max_length=10, blank=False, null=False)
    sDry=models.CharField(max_length=10, blank=False, null=False)
    sFold=models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        verbose_name = u"常用洗衣模式列表"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


class QRcode(models.Model):
    sOrderID=models.CharField(max_length=32, null=False, primary_key=True)
    sCodeA=models.CharField(max_length=20,blank=False, null=False)
    sCodeB=models.CharField(max_length=20,blank=False, null=False)

    class Meta:
        verbose_name = u"QRcode"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳

class Problem(models.Model):
    sOrderID=models.CharField(max_length=32, null=False)
    sSentTime=models.DateTimeField(default=datetime.now, blank=False, null=False)
    sDirections=models.TextField(blank=False, null=True)

    class Meta:
        verbose_name = u"問題回報"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


class Satisfy(models.Model):
    sOrderID=models.CharField(max_length=32, null=False, primary_key=True)
    sServe=models.BooleanField(blank=False, null=True)
    sRate=models.BooleanField(blank=False, null=True)
    sSatisfy=models.BooleanField(blank=False, null=True)

    class Meta:
        verbose_name = u"滿意度"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳

# Create your models here.

class Logindb(models.Model):
    sState=models.CharField(max_length=43, primary_key=True, default=wStateUUID)
    Rstate=models.CharField(max_length=42)
    RuserID=models.CharField(max_length=43)
    RSMSid=models.CharField(max_length=42)
    sPhone=models.CharField(max_length=10)
    Raccess_code=models.CharField(max_length=43)
    sTime=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name=u"Login紀錄"
        verbose_name_plural = verbose_name
