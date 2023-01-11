"""AI_Wash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from OrderApp import views

urlpatterns = [

    path('creditcard.html', views.creditcard_page),
    path('currentOrderInner.html', views.currentOrderInner_page),
    path('currentOrder.html', views.currentOrder_page),

    path('index.html', views.index_page),
    path('SACC_LineLoginURL', views.SACC_LineLoginURL),
    path('lineback', views.lineback),
    path('logout', views.logout),
    path('login.html', views.login_page),
    path('login_SMS1.html', views.login_SMS1_page),
    path('login_SMS2.html', views.login_SMS2_page),
    path('login_SMS3', views.login_SMS3),

    path('member.html', views.member_page),
    path('Add_UserMode', views.Add_UserMode),
    path('new.html', views.new_page),
    path('order_finish.html', views.order_finish_page),

    
    path('payNO.html', views.payNO_page),
    path('payOK.html', views.payOK_page),
    path('plzLogin.html', views.plzLogin_page),
    path('record.html', views.record_page),

    path('satisfaction.html', views.satisfaction_page),
    path('upload_satisfaction', views.upload_satisfaction),
    
    path('wash1.html', views.wash1_page),
    path('wash2.html', views.wash2_page),
    path('uber.html', views.uber_page),
    path('orderdata.html', views.orderdata_page),
    path('make_order', views.make_order),
    path('pay_finish.html', views.pay_finish_page),


]
