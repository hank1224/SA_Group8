from django.shortcuts import render, redirect
from django.conf import settings
from OrderApp.models import Delivery, Delivery_state
import datetime
from datetime import timedelta

def delivery_platfrom_page(request):
    update_states()
    URL = settings.NGROK+"/DeliveryApp"
    all_order = Delivery.objects.select_related().filter(sDelivery_Finish=False)
    
    return render(request, 'delivery_platfrom.html', locals())

def update_states():
    Delivery.objects.filter(sTakeTime__lte=datetime.datetime.now(), sDelivery_code=Delivery_state('0')).update(sDelivery_code=Delivery_state('1'))
    Delivery.objects.filter(sWashTime__lte=datetime.datetime.now(), sDelivery_code=Delivery_state('3')).update(sDelivery_code=Delivery_state('4'))
    Delivery.objects.filter(sReciveTime__lte=datetime.datetime.now(), sDelivery_code=Delivery_state('4')).update(sDelivery_code=Delivery_state('5'))

def updateto2(request):
    OrderID = request.GET.get('sOrderID')
    Delivery.objects.filter(sOrderID=OrderID).update(sDelivery_code=Delivery_state('2'))
    return redirect('delivery_platfrom.html')

def updateto3(request):
    OrderID = request.GET.get('sOrderID')
    Delivery.objects.filter(sOrderID=OrderID).update(sDelivery_code=Delivery_state('3'))
    return redirect('delivery_platfrom.html')

def updateto6(request):
    OrderID = request.GET.get('sOrderID')
    Delivery.objects.filter(sOrderID=OrderID).update(sDelivery_code=Delivery_state('6'))
    return redirect('delivery_platfrom.html')

def updatetodone(request):
    OrderID = request.GET.get('sOrderID')
    Delivery.objects.filter(sOrderID=OrderID).update(sDelivery_code=Delivery_state('7'), sDelivery_Finish=True)
    return redirect('delivery_platfrom.html')