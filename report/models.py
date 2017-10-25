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

    def GetSellTotal(self,startDate,endDate):
        curosr = connection.cursor()
        sqlStr = '''
                 SELECT a.sellDate, IFNULL(a.sellPrice,0), b.customer, IFNULL(ROUND((a.sellPrice/b.customer),0),0) as avgCustomer, ROUND((b.customer/7),2) as rate
                 FROM (SELECT date_format(entryTime,'%Y-%m-%d') as sellDate, SUM(sellPrice) as sellPrice FROM Sell_Basic  as a 
                 LEFT JOIN Sell as b  ON a.sellBasicId=b.sellBasicId WHERE isDelete=0 '''
        if not startDate == '':
            sqlStr += ''' AND entryTime > ' ''' + startDate + ''' 00:00:00 ' '''

        if not endDate == '':
            sqlStr += ''' AND entryTime < ' ''' + endDate + ''' 23:59:59 ' '''

        sqlStr += '''GROUP BY date_format(entryTime,'%Y-%m-%d')) as a
                 LEFT JOIN 
                 (SELECT date_format(entryTime,'%Y-%m-%d') as sellDate, SUM(customerNumber) as customer FROM Sell_Basic GROUP BY date_format(entryTime,'%Y-%m-%d')) as b
                 ON a.sellDate = b.sellDate
                '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['date'] = obj[0]
            dic['total'] = obj[1]
            dic['customer'] = obj[2]
            dic['avg'] = obj[3]
            dic['rate'] = obj[4]
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
                    WHERE c.Hour BETWEEN 12 AND 21
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

    def GetSellList(self,startDate,endDate):
        curosr = connection.cursor()
        sqlStr = '''          
                    SELECT sellNo, DATE_FORMAT(entryTime, '%Y-%m-%d %H:%i')  as entryTime, customerNumber, SUM(sellPrice) as total 
                    FROM Sell_Basic as a
                    LEFT JOIN Sell as b ON a.sellBasicId=b.sellBasicId
                    WHERE isDelete=0
                    '''

        if not startDate=='':
            sqlStr +='''AND a.entryTime > ' '''  + startDate + ''' 00:00:00 ' '''

        if not endDate == '':
            sqlStr += '''AND a.entryTime < ' ''' + endDate + ''' 23:59:59 ' '''

        sqlStr+='''  GROUP BY sellNo, entryTime, customerNumber ORDER BY sellNo;'''

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

    def Top10List(self):
        curosr = connection.cursor()
        sqlStr = '''
                 SELECT CONCAT(b.parentName,' - ',REPLACE(b.detailName,'<br>','')) as Name, a.sellQuantity
                 FROM (SELECT sellItem ,SUM(sellQuantity) as sellQuantity FROM Sell GROUP BY sellItem ORDER BY SUM(sellQuantity) DESC LIMIT 10) as a
                 LEFT JOIN (SELECT detailId, detailName, parentName FROM view_menu) as b ON a.sellItem=b.detailId
                '''
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['name'] = obj[0]
            dic['number'] = obj[1]
            result.append(dic)
        return result

class SellSum(models.Model):
    object = SellSumManager()
