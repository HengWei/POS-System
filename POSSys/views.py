from django.shortcuts import render
from POSSys.models import Menu, Sell, SellBasic, MenuAddition, SellTemp
from datetime import datetime
from django.utils import timezone


# Create your views here.

def index(request):
    # Set Basic Info
    basicInfo = SellBasic()
    basicInfo.entrytime = ''
    basicInfo.sellno = ''
    basicInfo.customernumber = ''
    sellbasicid = ''
    menuList = Menu.objects.filter(menuparentid=0)
    menu1 = Menu.objects.all().exclude(menuparentid=0)
    menuAddition = MenuAddition.objects.filter(menuadditionisdeletet=0).filter(menuadditionparentid=0)
    menuAdditionList = Menu.objects.filter(menuparentid__range=(1, 5))

    if request.method == 'POST':
        data = request.POST['sellList'].split(',')
        dataSell = Sell()
        dataSellTemp = SellTemp()
        if request.POST['txtSellBasicID'] == '':
            basicInfo.entrytime = request.POST['txtBasicInfoTime']
            basicInfo.sellno = request.POST['txtBasicInfoID']
            basicInfo.customernumber = request.POST['txtBasicInfoNumber']
            basicInfo.sellbasickeyindate = datetime.now()
            basicInfo.isdelete = 0
            basicInfo.save()
            sellbasicid = basicInfo.sellbasicid
        else:
            basicInfo = SellBasic.objects.get(sellbasicid=request.POST['txtSellBasicID'])
            # basicInfo.sellbasicid=request.POST['txtSellBasicID']
            sellbasicid = request.POST['txtSellBasicID']

        # 0:id 1:name 2:single price 3:amount 4:total price
        if request.POST['txtIsTemp'] == '0':
            for idx, val in enumerate(data):
                if (idx) % 5 == 0:
                    dataSell.sellitem = val
                if (idx) % 5 == 3:
                    dataSell.sellquantity = val
                if (idx) % 5 == 4:
                    dataSell.sellbasicid = basicInfo.sellbasicid
                    dataSell.selldatetime = datetime.now()

                    dataSell.sellprice = val
                    dataSell.sellhot = 0
                    dataSell.save()
                    dataSell.clean()
        else:
            for idx, val in enumerate(data):
                if (idx) % 5 == 0:
                    dataSellTemp.sellitem = val
                if (idx) % 5 == 3:
                    dataSellTemp.sellquantity = val
                if (idx) % 5 == 4:
                    dataSellTemp.sellbasicid = basicInfo.sellbasicid
                    dataSellTemp.sellprice = val
                    dataSellTemp.save()
                    dataSellTemp.clean()
                    basicInfo.sellno = ''
                    basicInfo.entrytime = ''
                    basicInfo.customernumber = ''
    return render(request, 'index.html', locals())


def Check(request):
    return render(request, 'check.html', locals())
