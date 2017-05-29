from django.db import models
from django.db import connection


# Create your models here.

class SellSumManager(models.Manager):
    def GetSellSumDetail(self):
        curosr = connection.cursor()
        sqlStr = '''
          SELECT Menu.menuParentId ,Menu.menuId, Menu.menuName, IFNULL(SUM(Sell.sellQuantity),0) as Number
          FROM Menu LEFT JOIN Sell ON Menu.menuId=Sell.sellItem
          WHERE Menu.menuParentId <> 0
          GROUP BY Menu.menuParentId, Menu.menuId, Menu.menuName
          ORDER BY Menu.menuParentId, Menu.menuId
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
          SELECT parentId ,parentName, IFNULL(SUM(Sell.sellQuantity),0) as Number
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


class SellSum(models.Model):
    object = SellSumManager()
