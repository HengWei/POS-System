from __future__ import unicode_literals

from django.db import models
from django.db import connection


# Create your models here.
class Menu(models.Manager):
    parentId = models.CharField(max_length=11)
    parentName = models.CharField(max_length=50)
    detailId = models.CharField(max_length=11)
    detailName = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=11, decimal_places=0)

    def GetList(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM view_menu;
        """)
        return [result[0] for result in cursor.fetchall()]
