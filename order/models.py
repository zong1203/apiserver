from django.db import models

# Create your models here.


class Order(models.Model):
    Order_ID = models.CharField(max_length=255, verbose_name='訂單UUID')
    Consumer = models.CharField(max_length=255, verbose_name='買家名稱')
    Provider = models.CharField(max_length=255, verbose_name='賣家名稱')
    Order = models.JSONField(verbose_name='訂單資訊')
    '''
    order: {
        '商品id': { amount: 數量, price: 單項金額 },
    }
    '''
    Totalprice = models.CharField(max_length=255, verbose_name='訂單總價格')
    Comment = models.CharField(max_length=255, verbose_name='買家留言',blank=True)
    Options = models.JSONField(verbose_name='買家提供的地點,時間')
    '''
    options: { //買家提供的時段
        start: [ '2023-07-07T12:00', '2023-07-08T10:00' ],
        end: [ '2023-07-14T12:00', '2023-07-14T13:00' ],
        position: [ '台科大 IB 1樓', '台科大 語言中心', '捷運公館 1號出口' ]
    }
    '''
    Selected_Option = models.JSONField(verbose_name='賣家選擇的地點,時間')
    '''
    selectedOption : { //賣家選擇的時間和地點
        start : "",
        end : "",
        position : ""
    }
    '''
    Using_Message = models.BooleanField(verbose_name='是否使用訊息討論交貨地點')
    Actual = models.JSONField(verbose_name='實際租借時間')
    '''
    actual : { //實際租借時間
        start : "",
        end : ""
    }
    '''
    Progress = models.IntegerField(verbose_name='訂單進度')
    """
    訂單進度
    不同身分在不同 progress 能做的操作不一樣
    0: 待確認
        買家：取消訂單
        賣家：取消訂單 確認訂單
    1: 待交貨
        買家：取消訂單 已收貨
        賣家：取消訂單
    2: 待歸還
        賣家：已歸還
    3: 已完成
    -1: 未完成
    """

    class Meta:
        db_table = "Order"
