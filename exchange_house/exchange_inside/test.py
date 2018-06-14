from selenium import webdriver
from bs4 import BeautifulSoup
#import DBA
import time,datetime
from exchange_rate import USDCNY


driver = webdriver.PhantomJS()
driver.get('https://www.bithumb.com/')
print(driver.title)
