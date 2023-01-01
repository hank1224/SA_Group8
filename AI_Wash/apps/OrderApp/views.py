from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages
from django.utils import timezone

from datetime import datetime, timedelta

from OrderApp.models import UserData, UserMode, Satisfy, OrderRecord
from DBmanageApp.models import ModeMenu



def creditcard_page(request):
    return render(request, template_name='creditcard.html')

def currentOrder_page(request):
    currentOrder=OrderRecord.objects.filter(sUserID="a1")
    for time in currentOrder:
        if time.sFinishTime > timezone.now():
            state="作業中"
        else :
            state="可領取"

    page=render(request,'currentOrder.html', locals())
    return page

def currentOrderInner_page(request):
    return render(request, template_name='currentOrderInner.html')

def index_page(request):
    page = render(request, template_name='index.html')
    return page if login_check(request) == True else login_check(request)

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
    if not "AIwash8" in request.session:
        request.session["AIwash8"] = True
        request.session.set_expiry(60*20) #存在20分鐘
        msg = "掛入AIwash8 session 效期20分鐘"
        respone = HttpResponse(msg + "<a href='/OrderApp/index.html'><h1>home</h1></a>")
    else:
        msg = "已存在session"
        respone = HttpResponse(msg + "<a href='/OrderApp/index.html'><h1>home</h1></a>")
    return respone

def del_session(request):
    try:
        del request.session["AIwash8"]
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

# Create your views here.
