from __future__ import unicode_literals

from django.db import models
from django.db import connection


class Menu(models.Model):
    menuid = models.IntegerField(db_column='menuId', primary_key=True)  # Field name made lowercase.
    menuname = models.CharField(db_column='menuName', max_length=50)  # Field name made lowercase.
    menuprice = models.IntegerField(db_column='menuPrice')  # Field name made lowercase.
    menuparentid = models.IntegerField(db_column='menuParentId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menu'
        app_label = 'POSSys'


class Sell(models.Model):
    sellid = models.BigIntegerField(db_column='sellId', primary_key=True)  # Field name made lowercase.
    sellbasicid=models.BigIntegerField(db_column='sellBasicId')
    sellitem = models.IntegerField(db_column='sellItem')  # Field name made lowercase.
    sellquantity = models.IntegerField(db_column='sellQuantity')  # Field name made lowercase.
    selldatetime = models.DateTimeField(db_column='sellDatetime', blank=True, null=True)  # Field name made lowercase.
    sellprice=models.IntegerField(db_column='sellPrice')
    sellhot=models.IntegerField(db_column='sellHot')

    class Meta:
        managed = False
        db_table = 'Sell'
        app_label = 'POSSys'


