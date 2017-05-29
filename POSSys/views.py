from django.shortcuts import render
from POSSys.models import Menu, Sell
from datetime import datetime
from django.utils import timezone


# Create your views here.

def index(request):
    menuList = Menu.objects.filter(menuparentid=0)
    menu1 = Menu.objects.all().exclude(menuparentid=0)
    if request.method == 'POST':
        data = request.POST['sellList'].split(',')
        dataSell = Sell()
        # 0:id 1:name 2:single price 3:amount 4:total price
        for idx, val in enumerate(data):
            if (idx) % 5 == 0:
                dataSell.sellitem = val
            if (idx) % 5 == 3:
                dataSell.sellquantity = val
            if (idx) % 5 == 4:
                dataSell.sellprice=val
                dataSell.sellbasicid = 0
                dataSell.sellhot=0
                dataSell.selldatetime = datetime.now()
                dataSell.save()
                dataSell.clean()
    return render(request, 'index.html', locals())


def Check(request):
    return render(request, 'check.html', locals())
