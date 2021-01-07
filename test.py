import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


if __name__ == '__main__':
    url = 'https://digital.cummins.com.cn/cip/home'
    driver = webdriver.Chrome('D:\dev\chromedriver_win32\chromedriver.exe')
    driver.get(url)


