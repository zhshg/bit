from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bit_api import *

# /browser/open 接口会返回 selenium使用的http地址，以及webdriver的path，直接使用即可
res = openBrowser()
driverPath = res['data']['driver']
debuggerAddress = res['data']['http']

print(driverPath)
print(debuggerAddress)

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)
dricer = webdriver.Chrome(driverPath, options=chrome_options)
dricer.get('https://www.baidu.com/')
