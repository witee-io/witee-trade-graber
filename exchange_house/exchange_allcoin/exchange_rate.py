#coding=utf-8

import requests
import json

# url = 'http://data.fixer.io/api/latest?access_key=2c523ab9f05824f786d33969ddc7155d'
# url = 'http://data.fixer.io/api/latest?access_key=2c523ab9f05824f786d33969ddc7155d&base = USD&symbols = GBP,JPY,EUR'
# headers = {
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# }
# response = requests.get(url, headers=headers)
# result = json.loads(response.text)
# print(result)
# USDCNY = result['rates']['CNY']
# print(USDCNY)

from forex_python.converter import CurrencyRates
c = CurrencyRates()
USDCNY = c.get_rates('usd')['CNY']
print(USDCNY)
