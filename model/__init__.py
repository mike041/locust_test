"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: __init__.py.py
@Site:
@time: 2022.11.09
"""
from selenium.webdriver.common.by import By

from env_config import group_name

phone_number = (By.ID, 'source')
privacy = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/label/span[1]/input')
login = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/form/div[2]/div/div/div/button/span')
i_know = (By.XPATH, '//*[@id="root"]/section/section/aside[1]/div/div/div[6]/div[2]/div/button/span')
popup_close = (By.XPATH, "/html/body/div[3]/div/div/div/a")
group = (By.XPATH, f"//span[text()='{group_name}']")
meeting_tip = (By.CLASS_NAME, 'meeting_tip')
join_meeting = (By.XPATH, "//span[text()='加入会议']")
leave_meeting = (By.XPATH, "//span[text()='退出会议']")
open_close_micro = (By.XPATH, '//*[@id="root"]/section/section/div[2]/div[2]/div[2]/div[1]/span[1]')


# class meeting:
#     meeting_has_joined = False
#     meeting_model = 'freedom'
#     microphone_on = False
