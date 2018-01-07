from __future__ import unicode_literals

from django.db import models
from django.db import connection


class MenuBack(models.Model):
    menuid = models.IntegerField(db_column='menuId', primary_key=True)  # Field name made lowercase.
    menuname = models.CharField(db_column='menuName', max_length=50)  # Field name made lowercase.
    menuprice = models.IntegerField(db_column='menuPrice')  # Field name made lowercase.
    menuparentid = models.IntegerField(db_column='menuParentId')  # Field name made lowercase.
    menuaddition = models.CharField(db_column='menuaddition', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BackupMenu'
        app_label = 'POSSys'

class Menu(models.Model):
    menuid = models.IntegerField(db_column='menuId', primary_key=True)  # Field name made lowercase.
    menuname = models.CharField(db_column='menuName', max_length=50)  # Field name made lowercase.
    menuprice = models.IntegerField(db_column='menuPrice')  # Field name made lowercase.
    menuparentid = models.IntegerField(db_column='menuParentId')  # Field name made lowercase.
    menuaddition = models.CharField(db_column='menuaddition', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menu'
        app_label = 'POSSys'


class Sell(models.Model):
    sellid = models.BigIntegerField(db_column='sellId', primary_key=True)  # Field name made lowercase.
    sellbasicid = models.BigIntegerField(db_column='sellBasicId')
    sellitem = models.IntegerField(db_column='sellItem')  # Field name made lowercase.
    sellquantity = models.IntegerField(db_column='sellQuantity')  # Field name made lowercase.
    selldatetime = models.DateTimeField(db_column='sellDatetime', blank=True, null=True)  # Field name made lowercase.
    sellprice = models.IntegerField(db_column='sellPrice')
    sellhot = models.IntegerField(db_column='sellHot')

    class Meta:
        managed = False
        db_table = 'Sell'
        app_label = 'POSSys'


class SellTemp(models.Model):
    sellid = models.BigIntegerField(db_column='sellId', primary_key=True)  # Field name made lowercase.
    sellbasicid = models.BigIntegerField(db_column='sellBasicId')
    sellitem = models.IntegerField(db_column='sellItem')  # Field name made lowercase.
    sellquantity = models.IntegerField(db_column='sellQuantity')  # Field name made lowercase.
    sellprice = models.IntegerField(db_column='sellPrice')

    class Meta:
        managed = False
        db_table = 'Sell_Temp'
        app_label = 'POSSys'


class SellBasic(models.Model):
    sellbasicid = models.AutoField(db_column='sellBasicId', primary_key=True)  # Field name made lowercase.
    sellno = models.CharField(db_column='sellNo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sellbasickeyindate = models.DateTimeField(db_column='sellBasicKeyinDate')  # Field name made lowercase.
    customernumber = models.IntegerField(db_column='customerNumber')  # Field name made lowercase.
    isdelete = models.IntegerField(db_column='isDelete')  # Field name made lowercase.
    entrytime = models.DateTimeField(db_column='entryTime')  # Field name made lowercase.
    istemp = models.IntegerField(db_column='isTemp')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Sell_Basic'
        app_label = 'POSSys'


class MenuAddition(models.Model):
    menuadditionid = models.IntegerField(db_column='menuAdditionId', primary_key=True)  # Field name made lowercase.
    menuadditionname = models.CharField(db_column='menuAdditionName', max_length=50)  # Field name made lowercase.
    menuadditionprice = models.IntegerField(db_column='menuAdditionPrice')  # Field name made lowercase.
    menuadditionisdeletet = models.IntegerField(db_column='menuAdditionIsDeletet')  # Field name made lowercase.
    menuadditionparentid = models.IntegerField(db_column='menuAdditionParentId')
    class Meta:
        managed = False
        db_table = 'Menu_Addition'
        app_label = 'POSSys'


class POSUser(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=150)  # Field name made lowercase.
    userloginid = models.CharField(db_column='userLoginID', max_length=255)  # Field name made lowercase.
    userloginpw = models.CharField(db_column='useLoginPW', max_length=255)  # Field name made lowercase.
    authority = models.IntegerField(db_column='Authority')
    class Meta:
        managed = False
        db_table = 'POSUser'
        app_label = 'POSSys'


class SellDetail(models.Manager):
    def GetSellDetail(self, sellNo):
        curosr = connection.cursor()
        sqlStr = '''
                SELECT sellId, CONCAT(view_menu.parentName,' - ',REPLACE(view_menu.detailName,'<br>','')) as Name
                , ROUND(sellPrice/sellQuantity,0) , sellQuantity,  sellPrice as income
                FROM Sell LEFT JOIN view_menu ON Sell.sellItem=view_menu.detailId 
                WHERE sellBasicId = ''' + sellNo
        curosr.execute(sqlStr)
        fetchall = curosr.fetchall()
        result = []
        for obj in fetchall:
            dic = {}
            dic['sellId'] = obj[0]
            dic['name'] = obj[1]
            dic['sellPrice'] = obj[2]
            dic['sellQuantity'] = obj[3]
            dic['income'] = obj[4]
            result.append(dic)
        return result

class SellData(models.Model):
    object = SellDetail()