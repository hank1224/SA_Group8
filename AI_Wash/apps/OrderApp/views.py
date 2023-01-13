from django.shortcuts import render ,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import requests

from datetime import datetime, timedelta

from OrderApp.models import *
from DBmanageApp.models import ModeMenu



def creditcard_page(request):
    return render(request, template_name='creditcard.html')

def login_page(request):
    return render(request, 'login.html')

def plzLogin_page(request):
    return render(request, template_name='plzLogin.html')

def login_SMS1_page(request):
    return render(request, 'login_SMS1.html')

@csrf_exempt
def login_SMS2_page(request):
    if request.method == 'POST':
        data = request.POST
        sphone = data.get('sPhone')
        if len(sphone) != 10 or sphone.startswith('09') != True:
            SMS_Auth_400 = True
            return render(request, 'login_SMS1.html', locals())

        # 欠重整判斷

        rurl = settings.SACC_NGROK+"/RESTapiApp/SMS_1"
        header = {
            'Authorization': 'Token '+settings.RESTAPI_TOKEN,
            'ngrok-skip-browser-warning': '7414'
        }
        param = {'Rphone':sphone}
        resb=requests.get(rurl,param,headers=header)

        if resb.status_code == 404:
            SMS_Auth_404 = True
            return render(request, 'login_SMS1.html', locals())

        rsmsid = resb.json()['RSMSid']
        print(resb.status_code)
        Logindb.objects.create(RSMSid=rsmsid, sPhone=sphone)

        return render(request, 'login_SMS2.html', locals())

@csrf_exempt
def login_SMS3(request):
    if request.method == 'POST':
        data = request.POST
        rsmsid = data.get('RSMSid')
        rcode = data.get('RSMS_code')
        sphone = data.get('sPhone')

        rurl = settings.SACC_NGROK+"/RESTapiApp/SMS_2"
        header = {
            'Authorization': 'Token '+settings.RESTAPI_TOKEN,
            'ngrok-skip-browser-warning': '7414'
        }
        param = {
            'RSMS_code': rcode,
            'RSMSid': rsmsid,
            }
        resb=requests.get(rurl,param,headers=header)
        print(resb.status_code)

        if resb.status_code != 200:
            SMS_Auth = False
            return render(request, 'login_SMS1.html', locals())
        
        ruserid = resb.json()['RuserID']
        raccess_code = resb.json()['Raccess_code']
        Logindb.objects.filter(RSMSid=rsmsid ,sPhone=sphone).update(Raccess_code=raccess_code, RuserID=ruserid)
        return Login_and_AddSession(request, ruserid, raccess_code)

def SACC_LineLoginURL(request):
    new_Logindb = Logindb.objects.create()
    sstate = new_Logindb.sState
    backurl = settings.NGROK+"/OrderApp/lineback?sState="+sstate

    rurl=settings.SACC_NGROK+"/RESTapiApp/Line_1"
    param={'Rbackurl':backurl}
    header={
        'Authorization': 'Token '+settings.RESTAPI_TOKEN,
        'ngrok-skip-browser-warning': '7414'
        }
    resb=requests.get(rurl,param,headers=header)
    rstate = resb.json()['Rstate']
    Logindb.objects.filter(sState=sstate).update(Rstate=rstate)
    url="https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1657781063&"+\
        "redirect_uri="+settings.SACC_NGROK+"/LineLoginApp/callback&state="+rstate+\
            "&scope=profile%20openid%20email&promot=consent&ui_locales=zh-TW"

    return HttpResponseRedirect(url)

def lineback(request):
    sstate = request.GET.get('sState')
    get_Rstate = Logindb.objects.get(sState=sstate)
    rstate = get_Rstate.Rstate

    rurl=settings.SACC_NGROK+"/RESTapiApp/Line_2"
    param={'Rstate': rstate}
    header={
        'Authorization': 'Token '+settings.RESTAPI_TOKEN,
        'ngrok-skip-browser-warning': '7414'
        }
    resb=requests.get(rurl,param,headers=header)

    ruserid = resb.json()['RuserID']
    raccess_code = resb.json()['Raccess_code']
    Logindb.objects.filter(sState=sstate ,Rstate=rstate).update(Raccess_code=raccess_code, RuserID=ruserid)
    return Login_and_AddSession(request, ruserid, raccess_code)

def Login_and_AddSession(request, userid, raccess_code):
    if 'AIwash8' in request.session:
        try:
            del request.session['AIwash8']
            del request.session['Raccess_code']
        except:
            pass
    request.session['AIwash8'] = userid
    request.session['Raccess_code'] = raccess_code
    request.session.modified = True
    request.session.set_expiry(60*30) #存在30分鐘
    try:
        UserData.objects.get(sUserID=request.session['AIwash8'])
    except ObjectDoesNotExist:
        UserData.objects.create(sUserID=request.session['AIwash8'])
        return HttpResponseRedirect('new.html')
    return HttpResponseRedirect('index.html')

def Access_API(request):
    raccess_code = request.session['Raccess_code']
    rurl=settings.SACC_NGROK+"/RESTapiApp/Access"
    param={'Raccess_code': raccess_code}
    header={
        'Authorization': 'Token '+settings.RESTAPI_TOKEN,
        'ngrok-skip-browser-warning': '7414'
        }
    resb=requests.get(rurl,param,headers=header)
    if resb.status_code == 409:
        print(resb.json())
        return False
    elif resb.status_code != 200:
        print(resb.json())
        return False
    sUser = resb.json()['sUser']
    sLineID = resb.json()['sLineID']
    sName = resb.json()['sName']
    sNickName = resb.json()['sNickName']
    sPhone = resb.json()['sPhone']
    sPhoneAuth = resb.json()['sPhoneAuth']
    sAddress = resb.json()['sAddress']
    sEmail = resb.json()['sEmail']
    sPictureUrl = resb.json()['sPictureUrl']
    print(resb.json())
    personal_data = {
        'Ruser':sUser,
        'Rlineid':sLineID,
        'Rname':sName,
        'Rnickname':sNickName,
        'Rphone':sPhone,
        'Rphoneauth':sPhoneAuth,
        'Raddress':sAddress,
        'Remail':sEmail,
        'Rpictureurl':sPictureUrl
    }
    return(personal_data)

def logout(request):
    try:
        del request.session['AIwash8']
        del request.session['Raccess_code']
    except:
        pass
    return HttpResponseRedirect('index.html')

def login_check(request):
    if not 'AIwash8' in request.session:
        return False
    elif 'AIwash8' in request.session:
        return True

def member_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        UserMode_data = UserMode.objects.filter(sUserID=request.session['AIwash8']).values()
        UserMode_items = []
        for usermode in UserMode_data:
            UserMode_items.append(usermode)
        
        page = render(request, 'member.html', locals())
    return page
    
@csrf_exempt
def Add_UserMode(request):
    if login_check(request) == False:
        return render(request, 'plzLogin.html')
    elif login_check(request) == True:
        if request.method == "POST":
            data = request.POST
            Wash = data.get('wash')
            Dry = data.get('dry')
            Fold = data.get('fold')
            ListName = data.get('listname')
            suserid = request.session['AIwash8']

            try:
                UserMode.objects.get(sUserID=UserData(suserid), sListName=ListName)
                try:
                    UserMode.objects.filter(sUserID=UserData(suserid), sListName=ListName).update(sWash=Wash, sDry=Dry, sFold=Fold)
                except:
                    HttpResponse("Updata err")
            except MultipleObjectsReturned:
                pass
            except ObjectDoesNotExist:
                UserMode.objects.create(sUserID=UserData(suserid), sListName=ListName, sWash=Wash, sDry=Dry, sFold=Fold)

            return redirect('member.html', permanent=True)

def new_page(request):
    return render(request, template_name='new.html')

def index_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        personal_data = Access_API(request)
        page = render(request, 'index.html', locals())
    return page


def order_finish_page(request):
    return render(request, template_name='order_finish.html')

def wash1_page(request):
    if login_check(request) == True:
        UserMode_data = UserMode.objects.filter(sUserID=request.session['AIwash8'])
        UserMode_items = []
        for usermode in UserMode_data:
            UserMode_items.append(usermode)
        page = render(request, 'wash1.html', locals())
    else:
        page = render(request, template_name='plzLogin.html')
    return page

def wash2_page(request):
    return render(request, template_name='wash2.html')

@csrf_exempt
def uber_page(request):
    if login_check(request) == True:
        personal_data = Access_API(request)
        if request.method == "POST":
            data = request.POST
            orderType = data.get('orderType')
            Wash = data.get('wash')
            Dry = data.get('dry')
            Fold = data.get('fold')
            
            datetime_now = (datetime.now()).strftime("%Y-%m-%dT%H:%M")
        
            a = OrderRecord.objects.filter(sUserID=request.session['AIwash8'])
            b = 0
            for i in a:
                b = 1
            First_wash = True if b == 0 else False

            ModeMenu_wash = ModeMenu.objects.filter(sModeName= Wash).values()
            ModeMenu_dry = ModeMenu.objects.filter(sModeName= Dry).values()
            ModeMenu_fold = ModeMenu.objects.filter(sModeName= Fold).values()
            sumTime = (ModeMenu_wash[0]['sTime'] + ModeMenu_dry[0]['sTime'] + ModeMenu_fold[0]['sTime'])
            sumTime_second = sumTime.total_seconds()
            datetime_washfinish = datetime.now() + sumTime

            page = render(request, 'uber.html', locals())
    else:
        page = render(request, template_name='plzLogin.html')
    return page

@csrf_exempt
def orderdata_page(request):
    if login_check(request) == True:
        if request.method == "POST":
            data = request.POST
            OrderType = data.get('orderType')
            Wash = data.get('wash')
            Dry = data.get('dry')
            Fold = data.get('fold')

            ModeMenu_wash = ModeMenu.objects.filter(sModeName= Wash).values()
            Wash_time = ModeMenu_wash[0]['sTime']
            Wash_price = float(ModeMenu_wash[0]['sPrice'])
            Wash_ppoint = float(ModeMenu_wash[0]['sPPoint'])
            Wash_carbon = float(ModeMenu_wash[0]['sCarbon'])

            ModeMenu_dry = ModeMenu.objects.filter(sModeName= Dry).values()
            Dry_time = ModeMenu_dry[0]['sTime']
            Dry_price = float(ModeMenu_dry[0]['sPrice'])
            Dry_ppoint = float(ModeMenu_dry[0]['sPPoint'])
            Dry_carbon = float(ModeMenu_dry[0]['sCarbon'])

            ModeMenu_fold = ModeMenu.objects.filter(sModeName= Fold).values()
            Fold_time = ModeMenu_fold[0]['sTime']
            Fold_price = float(ModeMenu_fold[0]['sPrice'])
            Fold_ppoint = float(ModeMenu_fold[0]['sPPoint'])
            Fold_carbon = float(ModeMenu_fold[0]['sCarbon'])

            sumTime = (Wash_time + Dry_time + Fold_time)
            sumPrice = int(Wash_price + Dry_price + Fold_price)
            sumPPoint = int(Wash_ppoint + Dry_ppoint + Fold_ppoint)
            sumCarbon = int(Wash_carbon + Dry_carbon + Fold_carbon)

            datetime_washfinish = datetime.now() + sumTime
            choose_time = []
            for i in range(5):
                a = datetime_washfinish+timedelta(hours=i*4)
                b = datetime_washfinish+timedelta(hours=(i+1)*4)
                choose_time.append(a.strftime("%d日 %H:00～")+b.strftime("%d日 %H:00"))

            Delivery = data.get('delivery')
            DTakeTime, DReciveTime, Address,TakeTime = "", "", "", ""
            if Delivery == "外送":
                DTakeTime=datetime.strptime(data.get('delivery_sent_time'), format("%Y-%m-%dT%H:%M"))
                DReciveTime=datetime.strptime(data.get('delivery_receive_time'), format("%Y-%m-%dT%H:%M"))
                Address=data.get('address')
                WashTime=DTakeTime + sumTime
            else:
                TakeTime=data.get('taketime')

            page = render(request, 'orderdata.html', locals())
    else:
        page = render(request, template_name='plzLogin.html')
    return page

@csrf_exempt
def make_order(request):
    if login_check(request) == True:
        if request.method == "POST":
            data = request.POST
            OrderType = data.get('orderType')
            Wash = data.get('wash')
            Dry = data.get('dry')
            Fold = data.get('fold')
            Carbon=data.get('carbon')
            Price=data.get('price')
            Point=data.get('point')

            sDelivery = data.get('delivery')

            if sDelivery == "外送":
                DTakeTime=datetime.strptime(data.get('delivery_sent_time'),format("%Y年%m月%d日 %H:%M"))
                DReciveTime=datetime.strptime(data.get('delivery_receive_time'),format("%Y年%m月%d日 %H:%M"))
                Address=data.get('address')
                WashTime=datetime.strptime(data.get('washtime'), format("%Y年%m月%d日 %H:%M"))

                new_record = OrderRecord.objects.create(sUserID=request.session['AIwash8'], sWash=Wash, sDry=Dry, sFold=Fold, \
                    sCarbon=Carbon, sSum=Price, sPoint=Point, sOrderType=OrderType, sDelivery=True)

                sOrderID = new_record.sOrderID
                Delivery.objects.create(sOrderID=OrderRecord(sOrderID), sTakeTime=DTakeTime, sReciveTime=DReciveTime, \
                    sAddress=Address, sDelivery_code=Delivery_state('0'), sWashTime=WashTime)
                page = render(request, 'uber_pay_finish.html', locals())
            else:
                TakeTime = data.get('orderTakeTime')
                FinishTime = datetime.strptime(data.get('finishtime'),format("%Y年%m月%d日 %H:%M"))
                OrderRecord.objects.create(sUserID=request.session['AIwash8'], sWash=Wash, sDry=Dry, sFold=Fold, sCarbon=Carbon, \
                sSum=Price, sPoint=Point, sOrderType=OrderType, sTakeTime=TakeTime, sFinishTime=FinishTime)
                page = render(request, 'pay_finish.html', locals())
    else:
        page = render(request, template_name='plzLogin.html')
    return page


def pay_finish_page(request):
    return render(request, template_name='pay_finish.html')

def currentOrder_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        currentOrder=OrderRecord.objects.filter(sUserID=request.session['AIwash8'], sFinish=False)


        page = render(request,'currentOrder.html', locals())
    return page

def currentOrderInner_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderID = request.GET.get('OrderID')
        OrderData = OrderRecord.objects.get(sOrderID=OrderID)
        DeliveryData, cline_display, sFinishTime= "", "", ""
        if OrderData.sDelivery == True:
            DeliveryData = Delivery.objects.get(sOrderID=OrderRecord(OrderID))
            cline_display = DeliveryData.sDelivery_code.cline_display
        else:
            fixTime = timedelta(hours=8)
            sFinishTime_done = False if (OrderData.sFinishTime.replace(tzinfo=None))+fixTime > datetime.now() else True
        page = render(request, 'currentOrderInner.html', locals())
    return page

def finish_order(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderID = request.GET.get('OrderID')
        OrderRecord.objects.filter(sOrderID=OrderID).update(sFinish=True)
        Order = OrderRecord.objects.get(sOrderID=OrderID)
        UserID = request.session['AIwash8']
        Point = Order.sPoint
        Carbon = Order.sCarbon
        Detail = "AIwash8訂單編號"+OrderID[-5:]
        API(UserID, Point, Carbon, Detail)
        if Order.sOrderType == 'pet':
            return render(request, 'satisfaction.html', locals())
        page = render(request, 'order_finish.html', locals())
    return page

def API(UserID, Point, Carbon, Detail):
    curl = settings.CARBON_NGROK
    resp = requests.post( curl + '/SA_ALL/news/history/', data = {
        "USER_PHONE": UserID, #userID
        "APP_ID": "AIwash8", #智慧喜＋之類的
        "DATE": datetime.now(),
        "POINT": Point,
        "DETAIL": Detail, #隨便打
        "TANPI": Carbon, #碳排放量（若你們沒有的話就一樣隨便打）
    })
    print(resp)
    # print(resp.json())

@csrf_exempt
def after_add_mode(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderData=""
        if request.method == 'POST':
            data = request.POST
            OrderID = data.get('orderid')
            ModeName = data.get('modename')
            OrderData = OrderRecord.objects.get(sOrderID=OrderID)
        if request.method == 'GET':
            OrderID = request.GET.get('OrderID')
            OrderData = OrderRecord.objects.get(sOrderID=OrderID)
        try:
            UserMode.objects.get(sListName=ModeName)
        except ObjectDoesNotExist:
            UserMode.objects.create(sListName=ModeName, sWash=OrderData.sWash, sDry=OrderData.sDry, \
                sFold=OrderData.sFold, sUserID=UserData(request.session['AIwash8']))
        page = render(request, 'satisfaction.html', locals())
    return page

def satisfaction_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderID=""
        if request.method == 'POST':
            data = request.POST
            OrderID = data.get('orderid')
        elif request.method == 'GET':
            OrderID = request.GET.get('OrderID')
        page = render(request, 'satisfaction.html', locals())
    return page

@csrf_exempt
def upload_satisfaction(request):
    if request.method == "POST":
        data = request.POST
        wServe = data.get('radio')
        wRate = data.get('radio_2')
        wSatisfy = data.get('radio_3')
        OrderID = data.get('orderid')

    if wServe == "F":
        wServe = False
    elif wServe == "T":
        wServe = True
    else:
        wServe = None

    if wRate == "F":
        wRate = False
    elif wRate == "T":
        wRate = True
    else:
        wRate = None

    if wSatisfy == "F":
        wSatisfy = False
    elif wSatisfy == "T":
        wSatisfy = True
    else:
        wSatisfy = None

    Satisfy.objects.create(sOrderID=OrderID, sServe= wServe, sRate= wRate, sSatisfy= wSatisfy)
    return render(request ,"satisfaction_result.html")

def record_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderRecords=OrderRecord.objects.filter(sUserID=request.session['AIwash8'], sFinish=True)
        page = render(request, 'record.html', locals())
    return page

def QA_page(request):
    OrderID = ""
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderID = request.GET.get('OrderID')
        page = render(request, 'QA.html', locals())
    return page

def payNO_page(request):
    return render(request, template_name='payNO.html')

def payOK_page(request):
    return render(request, template_name='payOK.html')




# Create your views here.
