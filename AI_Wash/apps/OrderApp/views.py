from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth

def creditcard_page(requset):
    return render(requset, template_name='creditcard.html')

def currentOrder_page(requset):
    return render(requset, template_name='currentOrder.html')

def currentOrderInner_page(requset):
    return render(requset, template_name='currentOrderInner.html')

def index_page(requset):
    return render(requset, template_name='index.html')

def member_page(requset):
    return render(requset, template_name='member.html')

def new_page(requset):
    return render(requset, template_name='new.html')

def order_finish_page(requset):
    return render(requset, template_name='order_finish.html')

def orderdata_page(requset):
    return render(requset, template_name='orderdata.html')

def pay_finish_page(requset):
    return render(requset, template_name='pay_finish.html')

def payNO_page(requset):
    return render(requset, template_name='payNO.html')

def payOK_page(requset):
    return render(requset, template_name='payOK.html')

def plzLogin_page(request):
    return render(request, template_name='plzLogin.html')

def record_page(requset):
    return render(requset, template_name='record.html')

def satisfacion_page(requset):
    return render(requset, template_name='satisfacion.html')

def wash1_page(requset):
    return render(requset, template_name='wash1.html')

def wash2_page(requset):
    return render(requset, template_name='wash2.html')


def session_check(requset):
    if not "vote" in requset.session:
        requset.session["vote"] = True
        requset.session.set_expiry(60*20) #存在20分鐘
        msg = "您第一次投票"
        respone = HttpResponse(msg)
    else:
        msg = "已投票"
        respone = HttpResponse(msg)
    return respone

def del_session(requset):
    try:
        del requset.session["vote"]
        return HttpResponse("Success")
    except:
        return HttpResponse("err")

def login_check(request):
    if not 'AIwash' in request.session:
        return HttpResponseRedirect('/plzLogin.html/')
    else:
        return HttpResponse("已登入")     

# Create your views here.
