from django.db import models

# Create your models here.

class Cart(models.Model):
    Account = models.CharField(max_length=20,  default='',verbose_name='用戶名稱')
    Commodity_ID = models.CharField(max_length=10,verbose_name='購物車商品ID')

    class Meta:
        db_table = "Cart"