from django.db import models
from django.db import connection

class SellListModel(models.Manager):
    def GetTempSell(self ,sellNo):
        curosr = connection.cursor()
        sqlStr = '''
          SELECT * 
          FROM (SELECT * 
          FROM Affogato.Sell_Temp 
          WHERE sellBasicId = (
          SELECT MAX(sellBasicId) 
          FROM Affogato.Sell_Basic 
          WHERE sellNo=''' + sellNo + ''')  AND isDelete=0) as t1
          LEFT JOIN Affogato.Menu as t2 ON ( t1.sellItem=t2.menuId);
        '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['sellItem'] = obj[2]
            dic['sellQuantity'] = obj[3]
            dic['sellPrice'] = obj[4]
            dic['menuName'] = obj[7]
            result.append(dic)
        return result



    def SellBasic(self ,sellNo):
        curosr = connection.cursor()
        sqlStr = '''
           SELECT * FROM Affogato.Sell_Basic WHERE sellBasicId = (
            SELECT MAX(sellBasicId) FROM Affogato.Sell_Basic WHERE sellNo=''' + sellNo + ''')
        '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result1 = []
        for obj in fetchall:
            dic = {}
            dic['sellNo'] = obj[1]
            dic['customerNumber'] = obj[3]
            dic['entryTime'] = obj[5]
            dic['sellBsicId'] = obj[0]
            result1.append(dic)
        return result1

    def SellTempList(self):
        curosr = connection.cursor()
        sqlStr = '''
                   SELECT sellBasicId, sellNo, customerNumber, entryTime FROM Sell_Basic WHERE sellBasicId IN (
                   SELECT sellBasicId FROM Sell_Temp WHERE isDelete=0 GROUP BY sellBasicId);
                '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['sellBasicId'] = obj[0]
            dic['sellNo'] = obj[1]
            dic['customerNumber'] = obj[2]
            dic['entryTime'] = obj[3]
            result.append(dic)
        return result


class Sell(models.Model):
    object = SellListModel()
