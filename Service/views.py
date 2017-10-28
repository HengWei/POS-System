from django.shortcuts import render
from django.http import HttpResponse
from Service.models import Sell
import json


# Create your views here.

def GetRecord(request):
    sellNo = request.GET['id']
    data = Sell.object.GetTempSell(sellNo)
    info = Sell.object.SellBasic(sellNo)
    infoData = []
    obj = []
    for item in data:
        obj.append([item['sellItem'], item['menuName'], item['sellPrice'], item['sellQuantity'], item['sellPrice']])

    for item2 in info:
        infoData.append([item2['sellBsicId'], item2['sellNo'], item2['customerNumber'],
                         item2['entryTime'].strftime("%Y-%m-%d %H:%M")])

    resultData = {'info': infoData, 'list': obj}

    result = json.dumps(resultData)
    return HttpResponse(result)


def GetTempList(request):
    data = Sell.object.SellTempList()
    obj = []
    for item in data:
        obj.append([item['sellItem'], item['menuName'], item['sellPrice'], item['sellQuantity'], item['sellPrice']])
    resultData = {'list': obj}
    result = json.dumps(resultData)
    return HttpResponse(result)

