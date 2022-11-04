"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: test_websocket
@Site:
@time: 2022.10.25
"""
import json
import time

import requests
from locust import task, HttpUser, User, events, constant, constant_pacing, TaskSet, LoadTestShape
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from MyWebsocket import MindWebSocket

from env_config import domain, group_id, group_name, receive_id, path, users

import queue

q = queue.Queue()

for user in users:
    q.put(user)


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--my-path", type=str, env_var="LOCUST_MY_PATH", default=path, help="It's working")
    parser.add_argument("--my-group", type=str, env_var="LOCUST_MY_GROUP", default=group_id, help="It's working")


class MindUser(User):
    http_client = None
    websocket_client = None
    user_id = None
    token = None
    wait_time = constant_pacing(10000)
    user = q.get()

    def on_start(self):
        self.http_client = requests.Session()
        url = f"https://{domain}/api/verifyUser/v2/login"
        payload = json.dumps({
            "source": str(self.user),
            "verifyLoginType": "phone",
            "countryZone": "+86",
            "module": "login",
            "platform": 3,
            "answerCode": "789456"
        })
        self.http_client.get(
            url=f'https://{domain}/api/verifyUser/getVerifyCode?source={self.user}&verifyLoginType=phone&countryZone=%2B86&module=login&platform=3')
        self.http_client.request("POST", url, data=payload)
        res = self.http_client.post(url=f'https://{domain}/api/imVerify/login', data={})
        cookie = requests.utils.dict_from_cookiejar(res.cookies)
        self.user_id = cookie['MINDIMUSERID']
        self.token = cookie['MINDIMTOKEN']
        print(self.token)

    @task
    def send_message(self):
        self.websocket_client = MindWebSocket(self.user_id,
                                              url=f'{path}/ws/web?sendID={self.user_id}&token={self.token}&platformID=5',
                                              group_id=group_id)

        self.websocket_client.run_forever()


class JoinLeaveMeetingUser(User):
    user = q.get()

    @task
    def join_leave_meeting(self):
        _options = Options()
        _options.set_capability('browserName', 'chrome')
        _options.add_argument('--no-sandbox')
        _options.add_argument('--disable-dev-shm-usage')
        # _options.add_argument('--headless')

        with webdriver.Chrome(options=_options) as driver:
            print('driver.session_id=======', driver.session_id)
            driver.maximize_window()
            driver.implicitly_wait(60 * 0.1)
            driver.get(f'https://{domain}/login')  # 注意测试环境改为http
            time.sleep(2)
            driver.find_element(By.ID, 'source').send_keys(self.user)
            while not driver.find_element(By.XPATH,
                                          '//*[@id="root"]/div/div[2]/div[2]/label/span[1]/input').is_selected():
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/label/span[1]/input').click()
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div[2]/div[2]/form/div[2]/div/div/div/button/span').click()
            time.sleep(1)
            ActionChains(driver).send_keys('789456').perform()
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/section/section/aside[1]/div/div/div[6]/div[2]/div/button/span').click()
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/a").click()
            driver.find_element(By.XPATH, f"//span[text()='{group_name}']").click()
            time.sleep(2)
            for i in range(10):
                driver.find_element(By.CLASS_NAME, 'meeting_tip').click()
                driver.find_element(By.XPATH, "//span[text()='加入会议']").click()
                time.sleep(2)
                driver.find_element(By.XPATH, "//span[text()='退出会议']").click()


class MicroPhoneUser(User):
    user = q.get()

    @task
    def open_close_microphone(self):
        _options = Options()
        _options.set_capability('browserName', 'chrome')
        _options.add_argument('--no-sandbox')
        _options.add_argument('--disable-dev-shm-usage')
        # _options.add_argument('--headless')

        with webdriver.Chrome(options=_options) as driver:
            print('driver.session_id=======', driver.session_id)
            driver.maximize_window()
            driver.implicitly_wait(60 * 0.1)
            driver.get(f'https://{domain}/login')  # 注意测试环境改为http
            time.sleep(2)
            driver.find_element(By.ID, 'source').send_keys(self.user)
            while not driver.find_element(By.XPATH,
                                          '//*[@id="root"]/div/div[2]/div[2]/label/span[1]/input').is_selected():
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/label/span[1]/input').click()
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/div/div[2]/div[2]/form/div[2]/div/div/div/button/span').click()
            time.sleep(1)
            ActionChains(driver).send_keys('789456').perform()
            time.sleep(1)
            driver.find_element(By.XPATH,
                                '//*[@id="root"]/section/section/aside[1]/div/div/div[6]/div[2]/div/button/span').click()
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/a").click()
            driver.find_element(By.XPATH, f"//span[text()='{group_name}']").click()
            driver.find_element(By.CLASS_NAME, 'meeting_tip').click()
            time.sleep(2)
            driver.find_element(By.XPATH, "//span[text()='加入会议']").click()
            for i in range(10):
                driver.find_element(By.XPATH,
                                    '//*[@id="root"]/section/section/div[2]/div[2]/div[2]/div[1]/span[1]').click()
                time.sleep(2)


