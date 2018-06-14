# coding: utf-8
from pymysql import *
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import pymysql
from DBUtils.PooledDB import PooledDB
from time import sleep

def get_data(pool):
    # conn = connect(host='192.168.0.252', port=3306, user='root', passwd='3bgaoshiqing', db='datacenter',
    #                charset='utf8mb4')
    # cursor = conn.cursor()
    conn = pool.connection()
    cursor = conn.cursor()

    sql = "select * from fxhprice order by replacetime desc limit 1"
    cursor.execute(sql)
    data=cursor.fetchall()
    time=data[0][-1]
    cursor.close()
    conn.close()
    return time

def send_email(now):
    nows = datetime.now()
    issure=nows-now
    issure=issure.total_seconds()
    if issure>=600:
        from_addr = '13619223983@163.com'
        password = '19951216hrr#'
        # 输入收件人地址:
        addrs = ['1660769848@qq.com', 'hlf0126@126.com', '531833345@qq.com','289942848@qq.com']
        for to_addr in addrs:
            # 输入SMTP服务器地址:
            smtp_server = 'smtp.163.com'

            msg = MIMEText('你好，你的非小号数据程序已停止，注意查看', 'plain', 'utf-8')
            msg['From'] = Header('<%s>' % from_addr, 'utf-8')
            msg['To'] = to_addr
            msg['Subject'] = Header('注意查看', 'utf-8')

            server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()


if __name__=='__main__':
    pool = PooledDB(pymysql, 1, 10, host='192.168.0.252', user='root', passwd='3bgaoshiqing', db='datacenter',port=3306)
    while True:
        try:
            now=get_data(pool)
            send_email(now)
            sleep(60)
        except:
            pass

