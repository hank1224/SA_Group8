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

def currentOrder_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        personal_data = Access_API(request)
        currentOrder=OrderRecord.objects.filter(sUserID=request.session['Raccess_code'], sFinishTime__isnull=True)

        for time in currentOrder:
            if time.sFinishTime > timezone.now():
                state= "作業中"
            else :
                state= "可領取"
        page = render(request,'currentOrder.html', locals())
    return page

def currentOrderInner_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        personal_data = Access_API(request)
        page = render(request, 'currentOrderInner.html', locals())
    return page

def index_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        personal_data = Access_API(request)
        page = render(request, 'index.html', locals())
    return page

def login_page(request):
    return render(request, 'login.html')

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



def member_page(request):
    if login_check(request) == True:
        UserMode_data = UserMode.objects.filter(sUserID=request.session['AIwash8']).values()
        UserMode_items = []
        for usermode in UserMode_data:
            UserMode_items.append(usermode)
        
        page = render(request, 'member.html', locals())
    else:
        page = login_check(request)
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

            ModeMenu_wash = ModeMenu.objects.filter(sModeName= Wash).values()
            ModeMenu_dry = ModeMenu.objects.filter(sModeName= Dry).values()
            ModeMenu_fold = ModeMenu.objects.filter(sModeName= Fold).values()
            sumTime = (ModeMenu_wash[0]['sTime'] + ModeMenu_dry[0]['sTime'] + ModeMenu_fold[0]['sTime'])
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

            
            Delivery = data.get('delivery')
            DTakeTime, DReciveTime, Address,TakeTime = "", "", "", ""
            if Delivery == "外送":
                DTakeTime=datetime.strptime(data.get('delivery_sent_time'), format("%Y-%m-%dT%H:%M"))
                DReciveTime=datetime.strptime(data.get('delivery_receive_time'), format("%Y-%m-%dT%H:%M"))
                Address=data.get('address')
            else:
                TakeTime=data.get('taketime')
            

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
            sumPrice = int(50 + Wash_price + Dry_price + Fold_price)
            sumPPoint = int(20 + Wash_ppoint + Dry_ppoint + Fold_ppoint)
            sumCarbon = int(Wash_carbon + Dry_carbon + Fold_carbon)

            datetime_washfinish = datetime.now() + sumTime
            choose_time = []
            for i in range(5):
                a = datetime_washfinish+timedelta(hours=i*4)
                b = datetime_washfinish+timedelta(hours=(i+1)*4)
                choose_time.append(a.strftime("%d日 %H:00～")+b.strftime("%d日 %H:00"))

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

                new_record = OrderRecord.objects.create(sUserID=request.session['AIwash8'], sWash=Wash, sDry=Dry, sFold=Fold, \
                    sCarbon=Carbon, sSum=Price, sPoint=Point, sOrderType=OrderType, sDelivery=True)

                sOrderID = new_record.sOrderID
                Delivery.objects.create(sOrderID=OrderRecord(sOrderID), sTakeTime=DTakeTime, sReciveTime=DReciveTime, \
                    sAddress=Address, sDelivery_code=Delivery_state('0'))
            else:
                TakeTime = data.get('takeTime')
                OrderRecord.objects.create(sUserID=request.session['AIwash8'], sWash=Wash, sDry=Dry, sFold=Fold, sCarbon=Carbon, \
                sSum=Price, sPoint=Point, sOrderType=OrderType, sTakeTime=TakeTime)

            



            page = render(request, 'pay_finish.html', locals())
    else:
        page = render(request, template_name='plzLogin.html')
    return page


def pay_finish_page(request):
    return render(request, template_name='pay_finish.html')

def payNO_page(request):
    return render(request, template_name='payNO.html')

def payOK_page(request):
    return render(request, template_name='payOK.html')

def plzLogin_page(request):
    return render(request, template_name='plzLogin.html')

def record_page(request):
    if login_check(request) == False:
        page = render(request, 'plzLogin.html')
    elif login_check(request) == True:
        OrderRecords=OrderRecord.objects.filter(sUserID=request.session['AIwash8'])
        page = render(request, 'record.html', locals())
    return page

def satisfaction_page(request):
    return render(request, template_name='satisfaction.html')

def upload_satisfaction(request):
    if login_check(request) == True:
        if request.method == "POST":
            data = request.POST
            wServe = data.get('radio')
            wRate = data.get('radio_2')
            wSatisfy = data.get('radio_3')

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

        Satisfy.objects.create(sOrderID="a2", sServe= wServe, sRate= wRate, sSatisfy= wSatisfy)
    else:
        return login_check(request)

    return render(request ,"satisfaction_result.html")

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

def test(request):
    a = UserData.objects.all()
    b = UserMode.objects.all()
    
    HttpResponse(str(a.union(b)))
# Create your views here.
