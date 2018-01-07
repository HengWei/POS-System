from django.shortcuts import render
from POSSys.models import Menu, Sell, SellBasic, MenuAddition, SellTemp, POSUser, SellData
from datetime import datetime
from django.http import HttpResponseRedirect
from django.db.models import Max


# Create your views here.

def index(request):
    # Set Basic Info
    if not LoginCheck(request):
        return HttpResponseRedirect('/login/')

    basicInfo = SellBasic()
    basicInfo.entrytime = ''
    basicInfo.sellno = ''
    basicInfo.customernumber = ''
    sellbasicid = ''
    basicInfo.istemp=0
    menuList = Menu.objects.filter(menuparentid=0)
    menu1 = Menu.objects.all().exclude(menuparentid=0)
    menuAddition = MenuAddition.objects.filter(menuadditionisdeletet=0).order_by('menuadditionname')
    menuAdditionList = Menu.objects.filter(menuparentid__range=(1, 5))
    menuAdditionList2 = Menu.objects.filter(menuparentid=12)


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
            dataSellBasic = SellBasic.objects.get(sellbasicid=basicInfo.sellbasicid)
            dataSellBasic.istemp = 0
            dataSellBasic.save()
            tempDate = dataSellBasic.entrytime.strftime("%Y/%m/%d %H:%M")

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
            dataSellBasic = SellBasic.objects.get(sellbasicid=basicInfo.sellbasicid)

            dataSellBasic.istemp = 1
            dataSellBasic.save()

    return render(request, 'index.html', locals())


def Check(request):
    return render(request, 'check.html', locals())



def LogOut(request):
    request.session.clear()
    return HttpResponseRedirect('/login/')
#
#
def LoginPage(request):
    if LoginCheck(request):
        return HttpResponseRedirect('/sell/')

    if request.method == 'GET':
        return render(request, 'login.html', locals())

    if request.method == 'POST':
        errorMessage = ''
        username = request.POST.get('inputName', '')
        password = request.POST.get('inputPassword', '')
        vaildate=POSUser.objects.filter(userloginid=username, userloginpw=password)
        if not vaildate:
            errorMessage = 'Sing in error!'
            return render(request, 'login.html', locals())
        else:
            searchResult=POSUser.objects.filter(userloginid=username, userloginpw=password).get()
            request.session['UserName'] = searchResult.username
            request.session['UserId']=searchResult.userid
            # request.session['UserPKID']=searchResult.employee_id
            # functionId = Prilivege.objects.filter(group_id__in=map(int, searchResult.group_pkid.split(','))).all()
            f = []
            # for item in functionId:
            #     f = list(set(f) | set(map(int, item.function_id.split(','))))
            # request.session['Auth'] = f
            return HttpResponseRedirect('/sell/')

def LoginCheck(request):

    if request.session.get('UserName', '') == '':
        return False
    else:
        return True


def MenuSetting(request):
    if not LoginCheck(request):
        return HttpResponseRedirect('/login/')

        return render(request, 'MenuSettingList.html', locals())

    menuList = Menu.objects.filter(menuparentid=request.GET['id'])
    return render(request, 'MenuSettingList.html', locals())

def MenuSettingDetail(request):
    if not LoginCheck(request):
        return HttpResponseRedirect('/login/')
    if request.method=='GET':
        menuParentList = Menu.objects.filter(menuparentid=0)
        menuAddition = MenuAddition.objects.filter(menuadditionisdeletet=0).order_by('menuadditionname')
        if request.GET['id'] == '0':
            menu = Menu()
            menu.menuid = ''
            menu.menuname = ''
            menu.menuparentid = 1
            menu.menuprice = 0
        else:
            menu = Menu.objects.get(menuid=request.GET['id'])
            if not menu.menuaddition == '':
                additionList = map(int, menu.menuaddition.split(','))
        return render(request, 'MenuSettingDetail.html', locals())

    else:
        if request.POST['menuId'] == '':
            menu = Menu()
            maxId=Menu.objects.filter(menuparentid=request.POST['menuParent']).aggregate(Max('menuid'))['menuid__max']
            if  maxId == None:
                menu.menuid=request.POST['menuParent']+'00'
            else:
                menu.menuid=maxId+1
            menu.menuname = request.POST['menuName']
            menu.menuparentid = request.POST['menuParent']
            menu.menuprice = request.POST['menuPrice']
            if not request.POST.get('GroupId', '') == '':
                menu.menuaddition= ','.join(request.POST.getlist('GroupId', 0))
            menu.save()
        else:
            menu = Menu.objects.get(menuid=request.POST['menuId'])
            menu.menuname = request.POST['menuName']
            if request.POST.get('menuParent', '') == '':
                menu.menuparentid='0'
            else:
                menu.menuparentid = request.POST['menuParent']
            menu.menuprice = request.POST['menuPrice']
            if not request.POST.get('GroupId', '') == '':
                menu.menuaddition= ','.join(request.POST.getlist('GroupId', 0))
            menu.save()
        return HttpResponseRedirect('/MenuSetting/?id='+menu.menuparentid)
    return render(request, 'MenuSettingDetail.html', locals())

def ModifyBasic(request):
    if not LoginCheck(request):
        return HttpResponseRedirect('/login/')

    if request.method == 'GET':
        data = SellBasic.objects.get(sellbasicid=request.GET['id'])
        entrtTime=data.entrytime.strftime('%Y//%m//%d %H:%m')
        keyinTime=data.sellbasickeyindate.strftime('%Y/%m/%d %H:%m')
        sellDetail=SellData.object.GetSellDetail(request.GET['id'])
        return render(request, 'ModifyBasic.html', locals())
    else:
        data = SellBasic.objects.get(sellbasicid=request.POST['sellbasicid'])
        data.sellno=request.POST['sellno']
        data.customernumber=request.POST['customernumber']
        data.entrytime=request.POST['datetimepicker4']
        # sellData=
        if request.POST.get('isDelete', False):
            data.isdelete = 1
        else:
            data.isdelete = 0
        data.save()
        return HttpResponseRedirect('/reportSellList/')


