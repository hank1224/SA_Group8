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
from apps.DeliveryApp import views

urlpatterns = [
    path('delivery_platfrom.html', views.delivery_platfrom_page),
    path('updateto2', views.updateto2),
    path('updateto3', views.updateto3),
    path('updateto6', views.updateto6),
    path('updatetodone', views.updatetodone),

]
