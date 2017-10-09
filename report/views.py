from django.shortcuts import render
from report.models import SellSum


# Create your views here.


def report(request):
    data = SellSum.object.GetSellSum()
    dataDetail=SellSum.object.GetSellSumDetail()
    return render(request, 'report.html', locals())

def reportSum(request):
    data = SellSum.object.GetSellTotal()
    return render(request, 'reportsum.html',locals())

def reportCustomer(request):
    data = SellSum.object.GetSellTime()
    return render(request, 'reportCustomer.html',locals())

def reportSellList(request):
    data= SellSum.object.GetSellList()
    return render(request, 'reportSellList.html',locals())