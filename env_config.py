"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: env_config
@Site:
@time: 2022.11.04
"""

# =======================================测试环境======================================================

# users = [15902379217, 15902379218, 15902379219, 15902379220, 15902379221, 15902379222, 15902379223]
# domain = 'mind.im30.lan'
#
# group_id = 'c5775d24e4f33ae29024323aa7822cf9'
# group_name = 'zyx创建全员1'
# receive_id = ''

# =======================================预发布环境======================================================
import queue

users = [15902379217, 15902379218]

domain = 'premind.im30.net'
group_id = '367694aea403361e2cd42377fd2bcd29'
group_name = '龙创（通知群）PRE'
receive_id = ''

path = 'wss://' + domain

q = queue.Queue()

for user in users:
    q.put(user)
