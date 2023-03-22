import datetime,random

now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))

r = now.hour*10000000+now.minute*100000+now.second*1000+now.microsecond%1000
print(r)
print(r*random.randrange(1,99999999))
print(r*random.randrange(1,99999999)%1000000000000)