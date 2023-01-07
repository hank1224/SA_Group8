from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
import requests

from datetime import datetime, timedelta

from OrderApp.models import *
from DBmanageApp.models import ModeMenu



def creditcard_page(request):
    return render(request, template_name='creditcard.html')

def currentOrder_page(request):
    currentOrder=OrderRecord.objects.filter(sUserID="a1",sFinishTime__isnull=True)

    for time in currentOrder:
        if time.sFinishTime > timezone.now():
            state= "作業中"
        else :
            state= "可領取"

    page = render(request,'currentOrder.html', locals())
    return page

def currentOrderInner_page(request):
    return render(request, template_name='currentOrderInner.html')

def index_page(request):
    page = render(request, template_name='index.html')
    return page if login_check(request) == True else login_check(request)

def login_page(request):
    return render(request, '1.html')

def SACC_LineLoginURL(request):
    new_LineLogin = LineLogin.objects.create()
    sstate = new_LineLogin.sState
    backurl = settings.NGROK+"/OrderApp/lineback?sState="+sstate

    rurl=settings.SACC_NGROK+"/RESTapiApp/Line_1"
    param={'Rbackurl':backurl}
    header={
        'Authorization': 'Token '+settings.RESTAPI_TOKEN,
        'ngrok-skip-browser-warning': '7414'
        }
    resb=requests.get(rurl,param,headers=header)
    rstate = resb.json()['Rstate']
    LineLogin.objects.filter(sState=sstate).update(Rstate=rstate)
    url="https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1657781063&"+\
        "redirect_uri="+settings.SACC_NGROK+"/LineLoginApp/callback&state="+rstate+\
            "&scope=profile%20openid%20email&promot=consent&ui_locales=zh-TW"

    return HttpResponseRedirect(url)

def lineback(request):
    sstate = request.GET.get('sState')
    get_Rstate = LineLogin.objects.get(sState=sstate)
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
    LineLogin.objects.filter(sState=sstate ,Rstate=rstate).update(Raccess_code=raccess_code, RuserID=ruserid)
    return Login_and_AddSession(request, ruserid, raccess_code)



def member_page(request):
    if login_check(request) == True:
        UserMode_data = UserMode.objects.filter(sUserID="a1").values()
        UserMode_items = []
        for usermode in UserMode_data:
            UserMode_items.append(usermode)
        
        page = render(request, 'member.html', locals())
    else:
        page = login_check(request)
    return page

def Add_UserMode(request):
    if request.method == "POST":
        data = request.POST
        Wash = data.get('wash')
        Dry = data.get('dry')
        Fold = data.get('fold')
        ListName = data.get('modelname')

        try:
            UserMode.objects.get(sUserID=UserData('a1'), sListName=ListName)
            try:
                UserMode.objects.filter(sUserID=UserData('a1'), sListName=ListName).update(sWash=Wash, sDry=Dry, sFold=Fold)
            except:
                HttpResponse("Updata err")
        except MultipleObjectsReturned:
            pass
        except ObjectDoesNotExist:
            UserMode.objects.create(sUserID=UserData("a1"), sListName=ListName, sWash=Wash, sDry=Dry, sFold=Fold)

        return HttpResponse("Su")


def new_page(request):
    return render(request, template_name='new.html')

def order_finish_page(request):
    return render(request, template_name='order_finish.html')

def orderdata_page(request):
    if login_check(request) == True:
        if request.method == "POST":
            data = request.POST
            Wash = data.get('wash')
            Dry = data.get('dry')
            Fold = data.get('fold')

            ModeMenu_wash = ModeMenu.objects.filter(sModeName= Wash).values()
            Wash_time = ModeMenu_wash[0]['sTime']
            Wash_price = float(ModeMenu_wash[0]['sPrice'])
            Wash_ppoint = float(ModeMenu_wash[0]['sPPoint'])

            ModeMenu_dry = ModeMenu.objects.filter(sModeName= Dry).values()
            Dry_time = ModeMenu_dry[0]['sTime']
            Dry_price = float(ModeMenu_dry[0]['sPrice'])
            Dry_ppoint = float(ModeMenu_dry[0]['sPPoint'])

            ModeMenu_fold = ModeMenu.objects.filter(sModeName= Fold).values()
            Fold_time = ModeMenu_wash[0]['sTime']
            Fold_price = float(ModeMenu_fold[0]['sPrice'])
            Fold_ppoint = float(ModeMenu_fold[0]['sPPoint'])

            sumTime = (Wash_time + Dry_time + Fold_time)
            sumPrice = int(50 + Wash_price + Dry_price + Fold_price)
            sumPPoint = int(20 + Wash_ppoint + Dry_ppoint + Fold_ppoint)

        page = render(request, 'orderdata.html', locals())
    else:
        page = login_check(request)
    return page


def pay_finish_page(request):
    return render(request, template_name='pay_finish.html')

def payNO_page(request):
    print('你爸')
    messages.error(request, '你是臭甲')
    print('你媽')
    # return render(request, 'payOK.html',locals())
    return HttpResponseRedirect("payOK.html")
    # return render(request, template_name='payNO.html')

def payOK_page(request):
    return render(request, template_name='payOK.html')

def plzLogin_page(request):
    return render(request, template_name='plzLogin.html')

def record_page(request):
    OrderRecords=OrderRecord.objects.filter(sUserID="a1")
    page=render(request, 'record.html', locals())
    return  page

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


def wash1_page(request):
    
    if login_check(request) == True:
        UserMode_data = UserMode.objects.filter(sUserID="a1").values()
        UserMode_items = []
        for usermode in UserMode_data:
            UserMode_items.append(usermode)
        page = render(request, 'wash1.html', locals())
    else:
        page = login_check(request)
    return page

def wash2_page(request):
    return render(request, template_name='wash2.html')



def new_session_check(request):
    if request.user.is_authenticated:
        account = request.user


def session_check(request):
    if not "Raccess_code" in request.session:
        request.session["Raccess_code"] = True
        request.session.set_expiry(60*10) #存在10分鐘
        msg = "掛入Raccess_code session 效期10分鐘"
        respone = HttpResponse(msg + "<a href='/OrderApp/index.html'><h1>home</h1></a>")
    else:
        msg = "已存在session"
        respone = HttpResponse(msg + "<a href='/OrderApp/index.html'><h1>home</h1></a>")
    return respone

def del_session(request):
    try:
        del request.session["Raccess_code"]
        return HttpResponse("Success del session")
    except:
        return HttpResponse("err")

def login_check(request):
    if not 'AIwash8' in request.session:
        check_return = render(request, template_name='plzLogin.html')
    elif 'AIwash8' in request.session:
        check_return = True
    else:
        check_return = HttpResponse("check_login err")
    return check_return


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
    request.session.set_expiry(20) #存在10分鐘
    return HttpResponseRedirect('index.html')

def test(request):
    a="N"
    b="N"
    try:
        a = request.session['AIwash8']
    except:
        pass
    try:
        b = request.session['Raccess_code']
    except:
        pass
    return HttpResponse("AIwash8: "+a+", Raccess_code: "+b)
# Create your views here.
