from django.db import models

# Create your models here.
class Commodity(models.Model):
    Launched = models.BooleanField(default=False,verbose_name='商品上架狀態')
    Img1 = models.CharField(max_length=45,verbose_name='圖片名稱(必須)')
    Img2 = models.CharField(max_length=45,blank=True,verbose_name='圖片名稱(可選)')
    Img3 = models.CharField(max_length=45,blank=True,verbose_name='圖片名稱(可選)')
    Img4 = models.CharField(max_length=45,blank=True,verbose_name='圖片名稱(可選)')
    Img5 = models.CharField(max_length=45,blank=True,verbose_name='圖片名稱(可選)')
    Name = models.CharField(max_length=45,verbose_name='商品名稱')
    Deacription = models.TextField(verbose_name='商品描述')
    Price = models.CharField(max_length=5,verbose_name='商品價格')
    Amount = models.CharField(max_length=5,verbose_name='商品數量')
    Position = models.TextField(verbose_name='商品位置')
    Account = models.CharField(max_length=20,  default='',verbose_name='賣場名稱')

    class Meta:
        db_table = "Commodity"

def search_by_commodity_keyword(keyword):
    if keyword:
        print(keyword)
        keyword_set = keyword.split(" ")
        commodity = []
        for keyword in keyword_set:
            commodity += Commodity.objects.filter(Name__contains=keyword,Launched=True)
        for i in commodity:
            flag = False
            for j,k in enumerate(commodity):
                if k == i:
                    if flag:
                        commodity.pop(j)
                        break
                    flag = True
        return commodity
    return []

def search_by_commodity_raw(**kwargs):
    commodity = kwargs.get('commodity')
    commodity_id = kwargs.get('commodity_id')
    account = kwargs.get('account')
    launched = kwargs.get('launched')
    if commodity:
        return Commodity.objects.raw(f'SELECT * FROM Commodity WHERE Name = "{commodity}"')
    elif commodity_id:
        return Commodity.objects.raw(f'SELECT * FROM Commodity WHERE id = "{commodity_id}"')
    elif account:
        return Commodity.objects.raw(f'SELECT * FROM Commodity WHERE Account = "{account}"')
    elif launched:
        return Commodity.objects.raw(f'SELECT * FROM Commodity WHERE Launched = true')
    else:
        return Commodity.objects.raw('SELECT * FROM Commodity')

def get_commodity_by_account(account):
    return Commodity.objects.filter(Account=account,Launched=True).values()