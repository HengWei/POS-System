from django.shortcuts import render
from report.models import SellSum
import datetime


# Create your views here.


def report(request):
    data = SellSum.object.GetSellSum()
    dataDetail=SellSum.object.GetSellSumDetail()
    top10List=SellSum.object.Top10List()
    return render(request, 'report.html', locals())

def reportSum(request):
    data = SellSum.object.GetSellTotal()
    return render(request, 'reportsum.html',locals())

def reportCustomer(request):
    data = SellSum.object.GetSellTime()
    return render(request, 'reportCustomer.html',locals())

def reportSellList(request):

    if request.method == 'GET':
        startDate=datetime.datetime.now().strftime('%Y//%m//%d')
        endDate= datetime.datetime.now().strftime('%Y//%m//%d')
    if request.method == 'POST':
        startDate=request.POST['startDate']
        endDate=request.POST['endDate']
    data= SellSum.object.GetSellList(startDate, endDate)
    return render(request, 'reportSellList.html',locals())