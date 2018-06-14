from bs4 import BeautifulSoup
import json
import PretendUrl


def get_Data(url):
    url_Data = PretendUrl.url(url)
    return url_Data


def findData():
    url = 'https://api.feixiaohao.com/coinhisdata/decent/'
    soup = BeautifulSoup(get_Data(url), 'lxml')
    soup = soup.text
    str_soup = ''.join(soup)
    print(type(str_soup))
    # res_json = json.loads(str_soup)
    # print(res_json['market_cap_by_available_supply'])
    # print()
    # print(res_json['price_btc'])
    # print()
    # print(res_json['price_usd'])
    # print()
    # print(res_json['vol_usd'])
    print(str_soup)


if __name__ == '__main__':
    findData()
