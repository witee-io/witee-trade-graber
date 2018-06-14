import requests
import pymysql
import time
from forex_python.converter import CurrencyRates
url1 = 'https://api.quoine.com/products'
def req():
    a = {}
    req1 = requests.get(url1)
    for i in req1.json():
        if i['quoted_currency'] == 'USD':
            a[i['base_currency']] = round(float(i['last_traded_price']),4)
    return a
def conn_mysql(names,exc_code,price,state):
    import uuid
    import datetime
    conn = pymysql.connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',charset='utf8mb4')
    cursor = conn.cursor()
    nows=datetime.datetime.now()
    now=nows.strftime('%Y-%m-%d %H:%M:%S')
    nows = nows.strftime('%Y%m')
    name = names + "_" + nows
    uid = str(uuid.uuid1()).replace('-','')
    try:
        sql = "create table exc_inside_" + name + "(name VARCHAR(50),exc_code VARCHAR(100), now_price VARCHAR(100),exchange_rate float,create_date datetime,uid VARCHAR(225),state int)"
        cursor.execute(sql)
        swl = "insert into exc_inside_" + name + "(name,exc_code,now_price,exchange_rate,create_date,uid,state)values('"+names+"','"+exc_code+"','"+ str(price)+"','"+str(USDCNY)+"','"+now+"','"+uid+"','"+str(state)+"')"
        cursor.execute(swl)
    except Exception as e:
        swl = "insert into exc_inside_" + name + "(name,exc_code,now_price,exchange_rate,create_date,uid,state)values('"+names+"','"+exc_code+"','"+str(price)+"','"+str(USDCNY)+"','"+now+"','"+uid+"','"+str(state)+"')"
        cursor.execute(swl)
    conn.commit()
    conn.close()
def sqlr(s):
    for i in s.keys():
        conn_mysql(i,'quoine',s[i],1)

if __name__ == '__main__':
    USDCNY = CurrencyRates().get_rates('usd')['CNY']
    while 1:
        try:
            sqlr(req())
            time.sleep(10)
            print('over')
        except Exception as e:
            print(e)
