from django.db import models
import hashlib

# Create your models here.

class Userfile(models.Model):
    Account = models.CharField(max_length=20)
    Password = models.CharField(max_length=65)
    Name = models.CharField(max_length=20)
    Email = models.CharField(max_length=40)
    Phonenumber = models.CharField(max_length=12,blank=True)
    StudentID = models.CharField(max_length=10)
    Introduction = models.TextField()
    Favorite = models.TextField()
    Profliephoto = models.CharField(max_length=50,  default='')

    class Meta:
        db_table = "Userfile"

class Chathistory(models.Model):
    Sender = models.CharField(max_length=20)
    Receiver = models.CharField(max_length=20)
    Type = models.CharField(max_length=10)
    Content = models.CharField(max_length=255)
    Date = models.CharField(max_length=10)
    Time = models.CharField(max_length=10)

    class Meta:
        db_table = "ChatHistory"

def get_nickname_by_account(account):
    a = Userfile.objects.filter(Account=account)
    return a[0].Name

def search_by_account_raw(**kwargs):
    account = kwargs.get('account')
    if account:
        result = Userfile.objects.raw('SELECT * FROM Userfile WHERE Account = %s',[account])
    else:
        result = Userfile.objects.raw('SELECT * FROM Userfile')
    return result

def jwt_search(account,password):
    result = Userfile.objects.raw(f'SELECT * FROM Userfile WHERE Account = "{account}"')
    if not result:
        return "尚未註冊"
    for r in result:
        if r.Password == hashlib.sha256(password.encode('utf-8')).hexdigest():
            return "ok"
    return "登入失敗"

def account_search(account):
    result = Userfile.objects.raw(f'SELECT * FROM Userfile WHERE Account = "{account}"')
    if not result:
        return "ok"
    return "帳號已經被註冊"

def get_primary_info_by_name(username):
    result = Userfile.objects.filter(Account=username)
    data = {
        "account": result[0].Account,
        "nickname": result[0].Name,
        "mail": result[0].Email,
        "phone":result[0].Phonenumber
    }
    return data