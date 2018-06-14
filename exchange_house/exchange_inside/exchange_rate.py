with open('get_rate/rate.txt', 'r', encoding = 'utf-8')as f:
    USDCNY = f.read().replace(',', '')


with open('get_rate/rate_krw.txt', 'r', encoding = 'utf-8')as f:
    USDKRW = f.read().replace(',', '')


