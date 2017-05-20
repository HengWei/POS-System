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
    sellitem = models.IntegerField(db_column='sellItem')  # Field name made lowercase.
    sellquantity = models.IntegerField(db_column='sellQuantity')  # Field name made lowercase.
    selldatetime = models.DateTimeField(db_column='sellDatetime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sell'
        app_label = 'POSSys'

# Create your models here.
# class view_menu(models.Manager):
#     parentId = models.CharField(max_length=11)
#     parentName = models.CharField(max_length=50)
#     detailId = models.CharField(max_length=11)
#     detailName = models.CharField(max_length=50)
#     price = models.DecimalField(max_digits=11, decimal_places=0)
#     class Meta:
#         managed = False
#         db_table = 'view_menu'
#
#
#     def GetList(self):
#         cursor = connection.cursor()
#         cursor.execute("""
#             SELECT *
#             FROM view_menu;
#         """)
#         return [result[0] for result in cursor.fetchall()]
