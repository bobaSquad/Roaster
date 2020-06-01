import datetime
from dateutil.parser import parse
from datetime import datetime, timedelta

date_time_str='2020-06-04T12:00:00+08:00'
time='2020-06-02T16:00:00+08:00'
# date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
# print(date_time_obj)

dt=parse(date_time_str)
print(dt.date())
datehw=str(dt.date())
print(type(dt.date()))
print(type(datehw))
timehw=parse(time)
print(timehw.time())
timehw=str(timehw.time())
# '2015-05-28T09:00:00-07:00'
print(datehw+"T"+timehw+'+08:00','final date')


ans=datehw+"T"+timehw+'+08:00'
dateu=parse(ans)
newdate=dateu+timedelta(hours=1)
print(newdate,'new lol')
newdate=str(newdate)
newdate=parse(newdate)
newdate=str(newdate.date())+"T"+str(newdate.time())+"+08:00"
print(newdate,"HAHA")