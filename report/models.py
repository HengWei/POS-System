from django.db import models
from django.db import connection


# Create your models here.

class SellSumManager(models.Manager):
    def GetSellSumDetail(self):
        curosr = connection.cursor()
        sqlStr = '''
        SELECT a.menuParentId,a.menuId,a.menuName , ROUND(IFNULL(a.Number/b.Number,0)*100,1) as Number 
        FROM (
        SELECT Menu.menuParentId ,Menu.menuId, Menu.menuName, IFNULL(SUM(Sell.sellQuantity),0) as Number
        FROM Menu LEFT JOIN Sell ON Menu.menuId=Sell.sellItem
        WHERE Menu.menuParentId <> 0
        GROUP BY Menu.menuParentId, Menu.menuId, Menu.menuName
        ORDER BY Menu.menuParentId, Menu.menuId) as a
        LEFT JOIN (SELECT Menu.menuParentId , IFNULL(SUM(Sell.sellQuantity),0) as Number
        FROM Menu LEFT JOIN Sell ON Menu.menuId=Sell.sellItem
        WHERE Menu.menuParentId <> 0
        GROUP BY Menu.menuParentId
        ) as b ON a.menuParentId=b.menuParentId 
        '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['parentId'] = obj[0]
            dic['menuId'] = obj[1]
            dic['menuName'] = obj[2]
            dic['number'] = obj[3]
            result.append(dic)
        return result

    def GetSellSum(self):
        curosr = connection.cursor()
        sqlStr = '''
          SELECT parentId ,parentName, ROUND((IFNULL(SUM(Sell.sellQuantity),0)/(SELECT SUM(Sell.sellQuantity)
          FROM Sell))*100,1) as Number 
          FROM view_menu LEFT JOIN Sell ON view_menu.detailId =Sell.sellItem
          GROUP BY parentId,parentName
          ORDER BY parentId
        '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['parentId'] = obj[0]
            dic['parentName'] = obj[1]
            dic['number'] = obj[2]
            result.append(dic)
        return result

    def GetSellTotal(self):
        curosr = connection.cursor()
        sqlStr = '''
                 SELECT date_format(entryTime,'%Y-%m-%d') as sellDate, SUM(sellPrice) FROM Sell_Basic as a 
                 LEFT JOIN Sell as b  ON a.sellBasicId=b.sellBasicId
                 GROUP BY date_format(entryTime,'%Y-%m-%d')
                '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['date'] = obj[0]
            dic['total'] = obj[1]
            result.append(dic)
        return result


    def GetSellTime(self):
        curosr = connection.cursor()
        sqlStr = '''
                    SELECT c.Hour, ifnull(b.num, 0) as num
                    FROM Code_Hour c
                    LEFT JOIN (
                    SELECT date_format(entryTime, '%k') as times, SUM(customerNumber) as num
                    FROM Sell_Basic
                    GROUP BY date_format(entryTime, '%k')) b ON c.Hour=b.times
                    ORDER BY c.Hour
                  '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['hour'] = obj[0]
            dic['num'] = obj[1]
            result.append(dic)
        return result

    def GetSellList(self):
        curosr = connection.cursor()
        sqlStr = '''          
                    SELECT sellNo, DATE_FORMAT(entryTime, '%Y-%m-%d %H:%i')  as entryTime, customerNumber, SUM(sellPrice) as total 
                    FROM Sell_Basic as a
                    LEFT JOIN Sell as b ON a.sellBasicId=b.sellBasicId
                    GROUP BY sellNo, entryTime, customerNumber
                    ORDER BY sellNo;                  
                  '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['sellNo'] = obj[0]
            dic['entryTime'] = obj[1]
            dic['customerNumber'] = obj[2]
            dic['income'] = obj[3]
            result.append(dic)
        return result



class SellSum(models.Model):
    object = SellSumManager()
