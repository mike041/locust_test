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
from locust import task, User, events, constant_pacing, TaskSet, HttpUser
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.MyWebsocket import MindWebSocket

from env_config import domain, group_id, group_name, path, users

import queue

q = queue.Queue()
for i in range(100):
    q.put(i)


# class TestUser(HttpUser):
#     host = ''
#     wait_time = constant_pacing(1)
#     user = q.get()
#     _options = Options()
#     _options.set_capability('browserName', 'chrome')
#     _options.add_argument('--no-sandbox')
#     _options.add_argument('--disable-dev-shm-usage')
#     # _options.add_argument('--headless')
#
#     driver = webdriver.Chrome(options=_options)
#
#     @task(1)
#     def task1(self):
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(60 * 0.1)
#         self.driver.get(f'https://www.baidu.com/s?w=1')  # 注意测试环境改为http
#         time.sleep(10)
#
#     @task(5)
#     def task2(self):
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(60 * 0.1)
#         self.driver.get(f'https://www.baidu.com/s?w=2')  # 注意测试环境改为http
#         time.sleep(10)


class TestUser(HttpUser):
    host = ''
    wait_time = constant_pacing(1)

    @task(1)
    def task1(self):
        user = q.get()

        print('开始任务', str(user))
        self.client.post(f'https://www.baidu.com/s?w={user}')  # 注意测试环境改为http
        print('结束任务', str(user))
    # @task(5)
    # def task2(self):
    #     self.driver.maximize_window()
    #     self.driver.implicitly_wait(60 * 0.1)
    #     self.driver.get(f'https://www.baidu.com/s?w={self.user}')  # 注意测试环境改为http
    #     time.sleep(10)
