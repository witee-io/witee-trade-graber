#coding=utf-8

import requests,json
import re,time
from email.mime.text import MIMEText
from email.header import Header
import smtplib
def get_data():
    url='http://1.85.6.34:8090/robot/getCoinByType?reqPara=tamibtc'
    # dat={
    #     "requestId": "2018030515143500112",
    #     "robotId": "wxid_twta46jpdrcv21",
    #     "sendId": "4826203122chatroom",
    #     "receiveId": "4552144486",
    #     "message": "tamibtc"
    #     }
    response=requests.get(url)
    result=eval(response.text)
    x=result['data']
    #print(x)
    type1=x['replyMessage'].split('-------------------------')
    seconds={}
    for i in type1[1:]:
        for j in i.split('\n')[1:]:
            pattern=re.compile(r'【(\d|\d+)秒前】')
            second=re.search(pattern,j)
            if second:
                name = j.split(':')[0]
                second=second.group(1)
                seconds[second]=name
                #if int(second)>=1000:
                    #seconds.append(j)
                    #print(j, second)
    return seconds
                    #print(j, second)
                    #send_email(name)

def send_email(now):
    print('发送邮件')
    from_addr = 'HH5318@126.com'
    password = 'huangfei123'
    # 输入收件人地址:
    addrs = ['1660769848@qq.com', 'hlf0126@126.com', '531833345@qq.com','289942848@qq.com']
    for to_addr in addrs:
        # 输入SMTP服务器地址:
        smtp_server = 'smtp.126.com'

        msg = MIMEText('你好，你的'+now+'程序已停止，注意查看', 'plain', 'utf-8')
        msg['Subject'] = '交易所监控'
        msg['From'] = Header('<%s>' % from_addr, 'utf-8')
        msg['To'] = to_addr
        msg['Subject'] = Header('注意查看', 'utf-8')

        server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    time.sleep(600)

def main():
    try:
        seconds=get_data()
        names=[]
        for x in seconds:
            print(x)
            if int(x)>=1000:
                names.append(seconds[x])
        print(names)
        if names!=[]:
            send_email(str(names).replace("[","").replace("]","").replace("'","").replace("'",""))
            #time.sleep(600)
    except Exception as e:
        print(e)
        pass    

if __name__=='__main__':
    while True:
        main()
        time.sleep(60)
