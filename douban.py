import json
import random
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains


class DoubanClient:
    base_url = 'https://accounts.douban.com/passport/login'
    driver_path = './driver/chromedriver.exe'
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print('load driver')
        self.driver = webdriver.Chrome(self.driver_path)
        self.header = {
            'Host': 'movie.douban.com',
            'Connection': 'keep-alive',
            'Content-Length': '52',
            'Accept': 'application/json',
            'Origin': 'https://movie.douban.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': '',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.login()

    def login(self):
        print('visit %s' % self.base_url)
        self.driver.get(self.base_url)
        self.driver.find_element_by_xpath('//div[@class="account-body-tabs"]/ul[1]/li[2]').click()
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//div[@class="account-form-field-submit "]/a').click()
        time.sleep(3)
        self._slide_()
        #self.driver.execute_script('return localStorage.getItem("token");')
        cookies = self.driver.get_cookies()
        self.cookie_parse = {}
        for c in cookies:
            self.cookie_parse[c['name']] = c['value']
        #self.driver.quit()

    '''
    to be complete 
    '''
    def write_diary(self, title, content):
        diary_url = 'https://www.douban.com/j/note/publish'
        note_text = {"blocks": [{ "key": "ff1231","text": content, "type": "unstyled", "depth": 0, "inlineStyleRanges": [],
                     "entityRanges": [], "data": {"page": 0}}], "entityMap": {}}
        req_data = {
            'is_rich': '1',
            'note_id': (str)(time.time()).split('.')[0],
            'note_title': title,
            'note_text': note_text,
            'introduction': '',
            'note_privacy': 'X',
            'cannot_reply': '',
            'author_tags': '',
            'accept_donation': '',
            'donation_notice': '',
            'is_original': '',
            'ck': self.cookie_parse['ck'],
            'action': 'new',
        }
        print(req_data)
        resp = requests.post(diary_url, req_data, headers=self.header, cookies=self.cookie_parse)
        print(resp)
        print(resp.text)

    def do_comment(self, comment):
        comment_url = 'https://movie.douban.com/j/subject/24741412/interest'
        req_data = {
            'ck': self.cookie_parse['ck'],
            'interest': 'collect',
            'rating': '',
            'foldcollect': 'F',
            'comment': comment,
            'private': 'on',
        }
        print(req_data)
        resp = requests.post(comment_url, req_data, headers=self.header, cookies=self.cookie_parse)
        print(resp)
        print(resp.text)

    def _slide_(self):
        self.driver.switch_to.frame(1)
        try:
            block = self.driver.find_element_by_id('tcaptcha_drag_thumb')
            reload = self.driver.find_element_by_id('reload')
        except NoSuchElementException as e:
            print('ERROR: %s, [Tip] if login success, then ignore this error.' % e)
            return

        total_time = 0

        while True:
            ActionChains(self.driver).click_and_hold(block).perform()
            ActionChains(self.driver).move_by_offset(180, 0).perform()
            tracks = self._get_track_(30)
            for track in tracks:
                print("move %s" % track)
                ActionChains(self.driver).move_by_offset(track, 0).perform()
            ActionChains(self.driver).release().perform()
            time.sleep(2)
            if self.driver.title == '登录豆瓣' and total_time < 5:
                print('failed, one more again!')
                reload.click()
                total_time += 1
                time.sleep(2)
            else:
                break



    def _get_track_(self,distance, rate=0.6, t=0.2, v=0):
        tracks = []
        # 加速减速的临界值
        mid = rate * distance
        # 当前位移
        s = 0
        # 循环
        while s < distance:
            # 初始速度
            v0 = v
            if s < mid:
                a = 20
            else:
                a = -3
            # 计算当前t时间段走的距离
            s0 = v0 * t + 0.5 * a * t * t
            # 计算当前速度
            v = v0 + a * t
            # 四舍五入距离，因为像素没有小数
            tracks.append(round(s0))
            # 计算当前距离
            s += s0

        return tracks