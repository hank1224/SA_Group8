from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, timedelta

from OrderApp.models import UserData, UserMode
from DBmanageApp.models import ModeMenu



def creditcard_page(request):
    return render(request, template_name='creditcard.html')

def currentOrder_page(request):
    return render(request, template_name='currentOrder.html')

def currentOrderInner_page(request):
    return render(request, template_name='currentOrderInner.html')

def index_page(request):
    page = render(request, template_name='index.html')
    #UserData.objects.create(sUserID = 'a2', sBag = 1, sUserMode = 1)
    return page if login_check(request) == True else login_check(request)

def member_page(request):
    return render(request, template_name='member.html')

def new_page(request):
    return render(request, template_name='new.html')

def order_finish_page(request):
    return render(request, template_name='order_finish.html')

def orderdata_page(request):
    if login_check(request) == True:

        Wash = request.GET.get('wash', "標準")
        Dry = request.GET.get('dry', "日曬")
        Fold = request.GET.get('fold', "機器人")

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
        sumPrice = int(Wash_price + Dry_price + Fold_price)
        sumPPoint = int(Wash_ppoint + Dry_ppoint + Fold_ppoint)


        page = render(request, 'orderdata.html', locals())
    else:
        page = login_check(request)    
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
    return render(request, template_name='record.html')

def satisfaction_page(request):
    return render(request, template_name='satisfaction.html')

def wash1_page(request):
    
    if login_check(request) == True:
        UserMode_data = UserMode.objects.filter(sUserID="a1").values()

        ListName_list=[]
        for usermode in UserMode_data:
            ListName_list.append(usermode['sListName'])

        page = render(request, 'wash1.html', locals())
    else:
        page = login_check(request)
    
    return page

def wash2_page(request):
    return render(request, template_name='wash2.html')








def session_check(request):
    if not "AIwash8" in request.session:
        request.session["AIwash8"] = True
        request.session.set_expiry(60*20) #存在20分鐘
        msg = "掛入AIwash8 session 效期20分鐘"
        respone = HttpResponse(msg)
    else:
        msg = "已存在session"
        respone = HttpResponse(msg)
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
