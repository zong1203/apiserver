from django.db import models

# Create your models here.
class Commodity(models.Model):
    Launched = models.BooleanField(default=False,verbose_name='商品上架狀態')
    Img1 = models.CharField(max_length=45)
    Img2 = models.CharField(max_length=45,blank=True)
    Img3 = models.CharField(max_length=45,blank=True)
    Img4 = models.CharField(max_length=45,blank=True)
    Img5 = models.CharField(max_length=45,blank=True)
    Name = models.CharField(max_length=45)
    Deacription = models.TextField()
    Price = models.CharField(max_length=5)
    Amount = models.CharField(max_length=5)
    Position = models.TextField()
    Account = models.CharField(max_length=20,  default='')

    class Meta:
        db_table = "Commodity"

def search_by_commodity_raw(**kwargs):
    commodity = kwargs.get('commodity')
    commodity_id = kwargs.get('commodity_id')
    account = kwargs.get('account')
    if commodity:
        result = Commodity.objects.raw(f'SELECT * FROM Commodity WHERE Name = "{commodity}"')
    elif commodity_id:
        result = Commodity.objects.raw(f'SELECT * FROM Commodity WHERE id = "{commodity_id}"')
    elif account:
        result = Commodity.objects.raw(f'SELECT * FROM Commodity WHERE Account = "{account}"')
    else:
        result = Commodity.objects.raw('SELECT * FROM Commodity')
    return result

def get_commodity_by_account(account):
    return Commodity.objects.filter(Account=account,Launched=True).values()