from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from DBmanageApp.models import ModeMenu, Store



def create_washMode(request):
    # try:

        delta = timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=30,
            hours=1,
            weeks=5
        )
        

        Modes = {
            'mode':[{
                'ModeName': '標準',
                'sTime': delta,
                'sPrice': 100,
                'sPPoint': 20,
            },{
                'ModeName': '精緻洗',
                'sTime': delta,
                'sPrice': 200,
                'sPPoint': 10,
            },{
                'ModeName': '柔洗',
                'sTime': delta,
                'sPrice': 150,
                'sPPoint': 8,
            },{
                'ModeName': '快洗',
                'sTime': delta,
                'sPrice': 80,
                'sPPoint': 15,
            }
            ]
        }
        
        for mode in Modes['mode']:
            ModeName = mode['ModeName']
            Time = mode['sTime']
            Price = mode['sPrice']
            PPoint = mode['sPPoint']
            ModeMenu.objects.create(sModeName=ModeName, sTime=Time, sPrice=Price, sPPoint=PPoint)
        daya = datetime.now() + delta

        return HttpResponse(daya)
    # except:
       # return HttpResponse("create Data err")

# Create your views here.
