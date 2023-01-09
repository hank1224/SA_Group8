from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from DBmanageApp.models import ModeMenu, Store

# 請幫我填上洗衣模式的 名稱、所需時間（timedelta）、價格、獲得點數

def create_washMode(request):
    try:

        # 都是選填的， = 0 的可以去除
        deltaA_1 = timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=30,
            hours=0,
            weeks=0
        )
        deltaA_2 = timedelta(
            minutes=50
        )
        deltaA_3 = timedelta(
            minutes=40
        )
        deltaA_4 = timedelta(
            minutes=20
        )
        deltaB_1 = timedelta(
            days=1
        )
        deltaB_2 = timedelta(
            hours=3
        )
        deltaB_3 = timedelta(
            hours=2
        )
        deltaB_4 = timedelta(
            hours=1
        )
        deltaC_1 = timedelta(
            hours=0
        )
        deltaC_2 = timedelta(
            minutes=20,
        )
        deltaD_1 = timedelta(
            minutes=20
        )
        deltaD_2 = timedelta(
            minutes=25
        )
        deltaD_3 = timedelta(
            minutes=30
        )
        deltaF_1 = timedelta(
            hours=1
        )
        deltaF_2 = timedelta(
            hours=0
        )

        Modes = {
            'mode':[{
                'ModeName': '標準',
                'sTime': deltaA_1,
                'sPrice': 50,
                'sPPoint': 25,
                'sCarbon': 1,
            },{
                'ModeName': '精緻洗',
                'sTime': deltaA_2,
                'sPrice': 55,
                'sPPoint': 20,
                'sCarbon': 2,
            },{
                'ModeName': '柔洗',
                'sTime': deltaA_3,
                'sPrice': 55,
                'sPPoint': 20,
                'sCarbon': 2,
            },{
                'ModeName': '快洗',
                'sTime': deltaA_4,
                'sPrice': 50,
                'sPPoint': 25,
                'sCarbon': 2,
            },{
                'ModeName': '日曬',
                'sTime': deltaB_1,
                'sPrice': 0,
                'sPPoint': 5,
                'sCarbon': 0,
            },{
                'ModeName': '低溫烘乾',
                'sTime': deltaB_2,
                'sPrice': 5,
                'sPPoint': 0,
                'sCarbon': 3,
            },{
                'ModeName': '中溫烘乾',
                'sTime': deltaB_3,
                'sPrice': 5,
                'sPPoint': 0,
                'sCarbon': 3,
            },{
                'ModeName': '高溫烘乾',
                'sTime': deltaB_4,
                'sPrice': 5,
                'sPPoint': 0,
                'sCarbon': 3,
            },{
                'ModeName': '不折',
                'sTime': deltaC_1,
                'sPrice': 0,
                'sPPoint': 5,
                'sCarbon': 0,
            },{
                'ModeName': '機器摺衣',
                'sTime': deltaC_2,
                'sPrice': 5,
                'sPPoint': 0,
                'sCarbon': 1,
            },{
                'ModeName': '一般洗淨',
                'sTime': deltaD_1,
                'sPrice': 0,
                'sPPoint': 5,
                'sCarbon': 1,
            },{
                'ModeName': '抗過敏洗淨',
                'sTime': deltaD_2,
                'sPrice': 10,
                'sPPoint': 0,
                'sCarbon': 1,
            },{
                'ModeName': '驅蟲洗淨',
                'sTime': deltaD_3,
                'sPrice': 15,
                'sPPoint': 0,
                'sCarbon': 2,
            },{
                'ModeName': '毛絮處理',
                'sTime': deltaF_1,
                'sPrice': 5,
                'sPPoint': 0,
                'sCarbon': 1,
            },{
                'ModeName': '無毛絮處理',
                'sTime': deltaF_2,
                'sPrice': 0,
                'sPPoint': 5,
                'sCarbon': 0,
            }]
        }
        
        for mode in Modes['mode']:
            ModeName = mode['ModeName']
            Time = mode['sTime']
            Price = mode['sPrice']
            PPoint = mode['sPPoint']
            Carbon = mode['sCarbon']
            ModeMenu.objects.create(sModeName=ModeName, sTime=Time, sPrice=Price, sPPoint=PPoint, sCarbon=Carbon)

        # daya = (datetime.now() + delta).strftime("%Y-%m-%d %H:%M:%S")
        # 時間加法範例，可預估完成時間

        return HttpResponse("<h1>Success</h1>")
    except:
       return HttpResponse("<h1>create Data err 請檢查是否已存在</h1>")

# Create your views here.
