from django.db import models

# Create your models here.

class Cart(models.Model):
    Account = models.CharField(max_length=20,  default='',verbose_name='用戶名稱')
    Seller = models.CharField(max_length=20,  default='',verbose_name='賣家名稱')
    Commodity_ID = models.CharField(max_length=10,verbose_name='購物車內商品ID')
    Commodity_Name = models.CharField(max_length=10,verbose_name='購物車內商品名稱',default="")

    class Meta:
        db_table = "Cart"