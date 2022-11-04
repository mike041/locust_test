"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: test
@Site:
@time: 2022.09.23
====================压测google分发token接口====================================
"""
import json
import time

from locust import task, FastHttpUser, constant_throughput, tag, LoadTestShape
from locust_plugins.users import SocketIOUser


class HelloWorldUser(FastHttpUser):
    wait_time = constant_throughput(1)
    host = 'http://34.110.138.72'

    @tag('google')
    @task
    def access_token(self):
        url = "/oauth/access_token"

        payload = {
            "package_name": "lf",
            "platform": "google"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.client.post(url, headers=headers, json=payload, verify=False)
        if response.status_code != 200:
            print(response.text)


class LoadShape(LoadTestShape):
    max_users = 100
    spawn_rate = 10
    max_time = 30 * 60

    def tick(self):
        run_time = self.get_run_time()
        current_user_count = self.get_current_user_count()
        print('run_time', run_time)
        print('current_user_count', current_user_count)
        if run_time < self.max_time:
            if self.get_current_user_count() < self.max_users:
                tick_data = (self.max_users, self.spawn_rate)
                return tick_data
            return (self.max_users, self.max_users)
        return None
