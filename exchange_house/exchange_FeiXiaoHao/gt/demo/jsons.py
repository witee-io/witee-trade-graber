# -*- coding: UTF-8 -*-
# python 解析json

import json

import requests

# url = "http://gthe.shop/coin/findAll";.
url = 'http://gthe.shop/coin/findBySymbol/btc'
param = {'action': '', 'start': '0', 'limit': '10000'}
return_data = requests.get(url, data=param).text
array = json.loads(return_data)
print(array['state'])
