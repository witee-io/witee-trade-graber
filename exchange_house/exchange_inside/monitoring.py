#coding=utf-8

from pymysql import *
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import pymysql,time
from DBUtils.PooledDB import PooledDB

def get_data():
    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='exchangedata',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool.connection()
    cursor = conn.cursor()

    sql = "select * from exc_inside_BTC201804 order by create_date desc limit 1"
    cursor.execute(sql)
    data=cursor.fetchall()
    times=data[0][4]
    cursor.close()
    conn.close()
    print(times)
    return times

def send_email():
    from_addr = 'HH5318@126.com'
    password = 'huangfei123'
        # 输入收件人地址:
    addrs = ['1660769848@qq.com', 'hlf0126@126.com', '531833345@qq.com']
    for to_addr in addrs:
            # 输入SMTP服务器地址:
        mtp_server = 'smtp.126.com'

        msg = MIMEText('你好，你的历史数据程序已停止，注意查看', 'plain', 'utf-8')
        msg['From'] = Header('<%s>' % from_addr, 'utf-8')
        msg['To'] = to_addr
        msg['Subject'] = Header('注意查看', 'utf-8')

        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()


if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='exchangedata',port=3306)
    while True:
        try:
            times=get_data()
            nows = datetime.now()
            issure=nows-times
            issure=issure.total_seconds()
            if issure>=200:
                send_email()
                while True:
                    time1=get_data()
                    if time1<200:
                        break
            time.sleep(60)
        except:
            pass
