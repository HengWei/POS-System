# !/usr/bin/python
# -*- coding:utf8 -*-

from django.shortcuts import render
from report.models import SellSum
from django.http import HttpResponse
import datetime
import csv



# Create your views here.


def report(request):
    data = SellSum.object.GetSellSum()
    dataDetail=SellSum.object.GetSellSumDetail()
    top10List=SellSum.object.Top10List()
    return render(request, 'report.html', locals())

def reportSum(request):
    if request.method == 'GET':
        startDate = (datetime.datetime.now()- datetime.timedelta(days=7)).strftime('%Y//%m//%d')
        endDate = datetime.datetime.now().strftime('%Y//%m//%d')
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
    data = SellSum.object.GetSellTotal(startDate, endDate)
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

def download_scv(request):

    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    encode = request.GET.get('encode', 'big5')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="SellIncom' + startDate+' to '+ endDate + '.csv"'

    writer = csv.writer(response, delimiter=',', quotechar='"')
    header = [u'日期', u'日收入', u'來客數', u'客均消費']
    writer.writerow([x.encode(encode) for x in header])
    deli = u'="{0}"'

    for i in SellSum.object.GetSellTotal(startDate, endDate):
        raw_row = [i['date'], i['total'], i['customer'], i['avg']]
        row = [deli.format(x).encode(encode) for x in raw_row]
        writer.writerow(row)
    return response