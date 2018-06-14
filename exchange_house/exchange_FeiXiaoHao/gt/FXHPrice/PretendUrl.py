# -*- coding: UTF-8 -*-
import requests


def url(url):
    try:
        # 伪装浏览器头....
        headers = {
            'Accept': 'application/json, text/javascript',
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        r = requests.get(url, headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"
