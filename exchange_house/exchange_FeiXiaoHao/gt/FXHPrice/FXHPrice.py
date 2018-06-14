# -*- coding: UTF-8 -*-
import sched
import time
import DBA
import Logs
from bs4 import BeautifulSoup
import PretendUrl


def changeDataAction():
    Logs.logger.info('changeDataAction')
    url = "https://www.feixiaohao.com/all"
    demo = PretendUrl.url(url)
    soup = BeautifulSoup(demo,'lxml')
    data_list = []
    for idx, tr in enumerate(soup.find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            rank = int(tds[0].contents[0])
            coinId = ''.join(tds[1].find('a')['href'].split('/')[1:][1]).lower()
            name = coinId.capitalize()
            symbol = tds[1].text.split('-')[0]
            marketcapcny = tds[2].text
            pricecny = tds[3].contents[0].text
            totalsupply = tds[4].text
            flow = tds[5].text
            hvolumecny = tds[6].text
            percentchange1h = tds[7].text
            percentchange24h = tds[8].text
            percentchange7d = tds[9].text
            t1 = time.time()
            sql = "REPLACE INTO fxhprice(rank,coinId,name,symbol,marketcapcny,pricecny,totalsupply,flow,hvolumecny,percentchange1h,percentchange24h,percentchange7d,replacetime) VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',now())"
            DBA.replaceObject(
                sql,
                rank,
                coinId,
                name,
                symbol,
                marketcapcny,
                pricecny,
                totalsupply,
                flow,
                hvolumecny,
                percentchange1h,
                percentchange24h,
                percentchange7d
            )
    Logs.logger.info('over')


# 初始化sched模块的scheduler类,第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)



# 被周期性调度触发的函数.
def execute_command(cmd, inc):
    changeDataAction()
    print('over')
    schedule.enter(inc, 0, execute_command, (cmd, inc))


def main(cmd, inc):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, execute_command, (cmd, inc))
    schedule.run()


# 每**秒查看下网络连接情况
if __name__ == '__main__':
    main("netstat -an", 5)

