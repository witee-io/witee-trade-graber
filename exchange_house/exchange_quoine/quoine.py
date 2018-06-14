import requests
import pymysql
import time
from forex_python.converter import CurrencyRates
url1 = 'https://api.quoine.com/products'
def req():
    a = {}
    req1 = requests.get(url1,timeout(10))
    for i in req1.json():
        if i['quoted_currency'] == 'USD':
            a[i['base_currency']] = round(float(i['last_traded_price']),4)
    return a
def sqlr(s):
    sql1 = '''replace into  exc_inside_realtime(name,exc_code,now_price,exchange_rate,create_date)VALUES(%s,%s,%s,%s,now())'''
    for i in s.keys():
        cursor1.execute(sql1, (i,'quoine',s[i],USDCNY ))
    conn1.commit()
if __name__ == '__main__':
    USDCNY = CurrencyRates().get_rates('usd')['CNY']
    while 1:
        conn1 = pymysql.connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',charset='utf8mb4')
        cursor1 = conn1.cursor()
        try:
            sqlr(req())
            time.sleep(10)
            print('over')
        except Exception as e:
            print(e)
        cursor1.close()
        conn1.close()
