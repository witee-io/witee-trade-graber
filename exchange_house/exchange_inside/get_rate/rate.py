import requests, time
import re


def get_usd_rate():
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E4%BA%BA%E6%B0%91%E5%B8%81&co=&resource_id=6017&t=1528510393791&cardId=6017&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery1102018281311158555114_1528510386271&_=1528510386273'
    header = {
        'Host': 'sp0.baidu.com',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=90066238_hao_pg&wd=%E6%B1%87%E7%8E%87%E6%9F%A5%E8%AF%A2&rsv_pq=d59755ec00003139&rsv_t=243dNT%2FvEFkOn1%2FByq2G%2FlXMchaqXvFhHlY5RhwD5ickiRNNhlj82c04eqAvqy2U9NvIYbIx&rqlang=cn&rsv_enter=1&rsv_sug3=25&rsv_sug1=21&rsv_sug7=100&rsv_sug2=0&inputT=14227&rsv_sug4=15427',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }
    while 1:
        try:
            req = requests.get(url=url, headers = header)
        except:
            print('汇率获取失败！')
            pass
        else:
            text = req.text
            re_1 = re.search('1美元=(.*?)人民币元', text)
            exchange_rate = re_1.group(1)
            with open('rate.txt', 'w+', encoding = 'utf-8')as f:
                f.write(exchange_rate)
            break


def get_krw_rate():
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E9%9F%A9%E5%85%83&co=&resource_id=4278&t=1528523299172&cardId=4278&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110203721287961638564_1528509799989&_=1528509800053'
    header = { 
        'Host': 'sp0.baidu.com',
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=90066238_hao_pg&wd=%E6%B1%87%E7%8E%87%E6%9F%A5%E8%AF%A2&rsv_pq=d59755ec00003139&rsv_t=243dNT%2FvEFkOn1%2FByq2G%2FlXMchaqXvFhHlY5RhwD5ickiRNNhlj82c04eqAvqy2U9NvIYbIx&rqlang=cn&rsv_enter=1&rsv_sug3=25&rsv_sug1=21&rsv_sug7=100&rsv_sug2=0&inputT=14227&rsv_sug4=15427',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }   
    while 1:
        try:
            req = requests.get(url=url, headers = header)
        except:
            print('汇率获取失败！')
            pass
        else:
            text = req.content.decode('unicode_escape')
            re_1 = re.search('1美元=(.*?)韩元', text)
            exchange_rate = re_1.group(1)
            with open('rate_krw.txt', 'w+', encoding = 'utf-8')as f:
                f.write(exchange_rate)
            break  



if __name__ == '__main__':
    while True:
            try:
                get_usd_rate()
                get_krw_rate()
                time.sleep(1200)
            except:
                pass
