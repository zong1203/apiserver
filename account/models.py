from django.db import models

# Create your models here.

class Userfile(models.Model):
    Account = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    Email = models.CharField(max_length=40)
    Phonenumber = models.CharField(max_length=12,blank=True)
    StudentID = models.CharField(max_length=10)
    Introduction = models.TextField()
    Favorite = models.TextField()
    Profliephoto = models.CharField(max_length=50,  default='', verbose_name='address')



    class Meta:
        db_table = "Userfile"

def search_by_account_raw(**kwargs):
    account = kwargs.get('account')
    if account:
        result = Userfile.objects.raw('SELECT * FROM Userfile WHERE Account = %s',[account])
    else:
        result = Userfile.objects.raw('SELECT * FROM Userfile')
    return result

def jwtsearch(account,password):
    result = Userfile.objects.raw(f'SELECT * FROM Userfile WHERE Account = "{account}"')
    if not result:
        return "account does not exist"
    for r in result:
        if r.Password == password:
            return "ok"
    return "password does not match"
