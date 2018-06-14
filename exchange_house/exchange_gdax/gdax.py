import requests
import json
import re, sys
sys.path.append("..")
from exchange_rate import USDCNY
import pymysql
import time
from DBUtils.PooledDB import PooledDB
#req = 'https://api.gdax.com/products'
#symbolid = requests.get(req).json()
#a=[]
#for i in symbolid:
#    b = re.split('-',i['id'])
#    if b[1] == 'USD':
#        a.append(b[0])
#print(a)
idlist1 = ['BCH', 'BTC', 'ETH', 'LTC']
def sqlr(s):
    conn1 = pool.connection()
    cursor1 = conn1.cursor()
    sql1 = '''replace into  exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
    for i in s.keys():
        cursor1.execute(sql1, (i,'gdax',s[i],USDCNY ))
    conn1.commit()
    conn1.close()
def trad1():
    s1 = {}
    for i in idlist1:
        t = requests.get('https://api.gdax.com/products/'+i+'-USD/trades',timeout = 5).json()[1]
        s1[i] = float(t['price'])
    return s1
if __name__ == '__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306) 
    while 1:
        try:
            sqlr(trad1())
            print('over')
            time.sleep(10)
        except Exception as e:
            print(e)
#    threads=[]
#    i=0
#    j=50
#    while j <= 38000:
#    for x in range(i,j):
#    n=600+x
#    t=threading.Thread(target=gg,args=(n,))
#    threads.append(t)
#    print(threads)
#    for y in range(i,j):
#    threads[y].start()
#    for y in range(i,j):
#    threads[y].join()
#    i=i+50
#    j=j+50
