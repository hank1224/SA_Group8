from django.db import models


class ModeMenu(models.Model):
    sModeName=models.CharField(max_length=10,blank=False, null=False)
    sTime=models.DurationField(blank=False, null=True)
    sPrice=models.FloatField(blank=False, null=True)
    sPPoint=models.FloatField(blank=False, null=True)

    class Meta:
        verbose_name = u"洗衣模式價格表"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


class Store(models.Model):
    sStoreID=models.CharField(max_length=32, null=False, primary_key=True)
    sStoreName=models.CharField(max_length=10, blank=False, null=False)
    sStoreAdd=models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = u"店鋪"
        verbose_name_plural = verbose_name
    
    #def __str__(self):
        #return self.sLocationName
    #讓object預設回傳


# Create your models here.
