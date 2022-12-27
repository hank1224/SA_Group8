from django.db import models
from datetime import datetime

class OrderRecord(models.Model):
    sOrderID=models.CharField(max_length=32, null=False, primary_key=True)
    sUserID=models.CharField(max_length=32, null=False)
    sSum=models.FloatField(blank=False, null=False)
    sPoint=models.FloatField(blank=False, null=False)
    sCreateTime=models.DateTimeField(default=datetime.now, blank=False, null=True)
    sFinishTime=models.DateTimeField(blank=False, null=True)
    sStoreName=models.CharField(max_length=10,blank=False, null=False)
    
    class Meta:
        verbose_name = u"訂單記錄"
        verbose_name_plural = verbose_name

    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


class UserData(models.Model):
    sUserID=models.CharField(max_length=32, null=False, primary_key=True)
    sBag=models.PositiveIntegerField(blank=False ,null=False, default=0)
    sUserMode=models.PositiveIntegerField(blank=False, null=True)

    class Meta:
        verbose_name = u"顧客資料"
        verbose_name_plural = verbose_name

    #def __str__(self):
        #return self.sUserID
    #讓object預設回傳


class Mode(models.Model):
    sOrderID=models.CharField(max_length=32, null=False, primary_key=True)
    sWash=models.PositiveIntegerField(blank=False, null=False)
    sDry=models.PositiveIntegerField(blank=False, null=False)
    sFold=models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        verbose_name = u"訂單洗衣設定"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


class ModeMenu(models.Model):
    sModeID=models.CharField(max_length=32, null=False, primary_key=True)
    sModeName=models.CharField(max_length=10,blank=False, null=False)
    sTime=models.TimeField(blank=False, null=False)
    sAmount=models.FloatField(blank=False, null=False)
    sPPoint=models.FloatField(blank=False, null=False)

    class Meta:
        verbose_name = u"洗衣模式價格表"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳

class Common(models.Model):
    sCommonID=models.CharField(max_length=32, null=False, primary_key=True)
    sListName=models.CharField(max_length=10,blank=False, null=False)
    sWash=models.PositiveIntegerField(blank=False, null=False)
    sDry=models.PositiveIntegerField(blank=False, null=False)
    sFold=models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        verbose_name = u"常用洗衣模式列表"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


class Store(models.Model):
    sStoreID=models.CharField(max_length=32, null=False, primary_key=True)
    sStoreName=models.CharField(max_length=10,blank=False, null=False)
    sStoreAdd=models.CharField(max_length=100,blank=False, null=False)

    class Meta:
        verbose_name = u"店鋪"
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
    sProblemID=models.CharField(max_length=32, null=False, primary_key=True)
    sOrderID=models.CharField(max_length=32, null=False)
    sSentTime=models.DateTimeField(default=datetime.now, blank=False, null=False)
    sDirections=models.CharField(max_length=300,blank=False, null=False)


    class Meta:
        verbose_name = u"問題回報"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳

class Satisfy(models.Model):
    sOrderID=models.CharField(max_length=32, null=False, primary_key=True)
    sServe=models.BooleanField(blank=False, null=False)
    sRate=models.BooleanField(blank=False, null=False)
    sSatisfy=models.BooleanField(blank=False, null=False)

    class Meta:
        verbose_name = u"滿意度"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳

# Create your models here.
