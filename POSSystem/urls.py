"""POSSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
from POSSys.views import index, LoginPage, LogOut, MenuSetting, MenuSettingDetail
from report.views import report, reportSum, reportCustomer, reportSellList
from Service.views import GetRecord

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^sell/', index),
    url(r'^reportSum/$', reportSum),
    url(r'^reportCustomer/$', reportCustomer),
    url(r'^report/$', report),
    url(r'^getRecord/$', GetRecord),
    url(r'^login/$', LoginPage),
    url(r'^logout/$', LogOut),
    url(r'^reportSellList/$', reportSellList),
    url(r'^MenuSetting/$', MenuSetting),
    url(r'^MenuSettingDetail/$', MenuSettingDetail),

]
