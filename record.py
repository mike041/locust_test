"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: record
@Site:
@time: 2024.05.18
"""
import json
import os
from datetime import datetime
from time import sleep

import pandas as pd
import requests

df = pd.read_excel('私聊+id.xlsx')
folder_path = './'
file_path = './new_file'


def get_recv_id(conversation_id):
    return str(conversation_id).split('_')[-1]


def get_single_recv_id(conversation_id):
    li = (conversation_id).split('_')
    if len(li) > 2:
        return str(li[1]) + "_" + str(li[2])
    else:
        return li[-1]


def get_record(conversation_id):
    all_record = []
    overtime_record = []
    original_res = []
    API_URL = "https://mind-api.im30.net/api/search/im/chat/search"
    recv_id = get_single_recv_id(conversation_id)
    PER_PAGE = 50
    # 初始化变量
    page = 1

    # 发送请求并获取总条目数
    payload = {
        "session_type": 1,
        "content_type": 101,
        "search_text": "",
        "page": 1,
        "size": 50,
        "send_id": "ahorzam3ypfa9xyw_gi94cns4b38wtcz5",
        "recv_id": recv_id,
        "operator": "ahorzam3ypfa9xyw_gi94cns4b38wtcz5",
        "group_member_ids": [
            "ahorzam3ypfa9xyw_gi94cns4b38wtcz5"
        ],
        "conversation_id": conversation_id
    }
    headers = {
        'team-id': '5',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'x-token': 'Q_npVRffBGaQycG7_63Mugx7L9BakCw4rbmJEcXzB8FI7TlU303MvzGVyCTyxtnJ',
        'sec-ch-ua-mobile': '?0',
        'im-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVSUQiOiJhaG9yemFtM3lwZmE5eHl3X2dpOTRjbnM0YjM4d3RjejUiLCJQbGF0Zm9ybSI6IldlYiIsImV4cCI6MjAzMDQxMzczMiwibmJmIjoxNzE1MDUzNDMyLCJpYXQiOjE3MTUwNTM3MzJ9.NgQpyRR5Q17dkAGLrhwSqSTcES1TX4yMhgJ36SnOPR0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'device-id': '5a0767faeee9c7c39a99cd804b8df5db',
        'Referer': '',
        'sw8': '1-NzRmZmZmMzYtNWQ2NS00Yzc2LWI4MWUtNjg3MDQ4ZjgyMjgz-ZmI4YWFlM2EtNmI2Yi00ZjNmLWI5OGEtYTcwOWNiMWRlNjFh-1-YWVnaXM=-MS4zNy44-Lw==-bWluZC5pbTMwLm5ldA==',
        'x-request-id': 'h4d80bljb1716006330038ahorzam3ypfa9xyw',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        total = response.json()['data']['total']  # 假设响应的JSON中包含total字段
        if total > 0:
            print(f"Total items: {total}")
        else:
            print("No data available.")
    else:
        print(f"Failed to fetch data: {response.status_code}")
        total = 0

    # 分页获取数据
    while page <= total // PER_PAGE + (1 if total % PER_PAGE else 0):
        payload['page'] = page
        response = requests.request("POST", API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:

            for chat in response.json()['data']['chats']:
                # 提取createTime和content
                createTime = chat['msg']['createTime']
                content = chat['msg']['content']
                single_chat = {
                    'createTime': str(datetime.fromtimestamp(createTime / 1000).strftime('%Y-%m-%d %H:%M:%S')),
                    'content': content
                }
                original_res.append(response.json())
                all_record.append(single_chat)

                # 将提取的信息添加到结果列表中
                if (datetime.fromtimestamp(createTime / 1000).hour >= 19 or datetime.fromtimestamp(
                        createTime / 1000).hour < 6):
                    overtime_record.append(single_chat)
                    # 打印结果
                    # print("Filtered Timestamps (between 19:00 and 6:00):",
                    #       str(datetime.fromtimestamp(createTime / 1000).strftime('%Y-%m-%d %H:%M:%S')), content)
        else:
            print(f"Failed to fetch data on page {page}: {response.status_code}")

        # 更新页码
        page += 1
    return original_res, all_record, overtime_record


def export_excel(record: list, name: str, path='./'):
    # 保存为Excel格式
    # 假设all_data是一个列表的列表或者字典的列表
    # 如果是字典列表，需要先将其转换为DataFrame
    if record and isinstance(record[0], dict):
        df = pd.DataFrame(record)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, name)
        df.to_excel(file_path, index=False)
    else:
        pd.DataFrame(record).to_excel(name + '.xlsx', index=False)
    print("Data saved as Excel.")


for index, row in df.iterrows():
    folder_name = row['name'].replace(' ', '_').replace('/', '_').replace('\\', '_')
    folder_path = os.path.join('E:\\download\\record', folder_name)
    _conversation_id = row['conversation_id']
    original_res, all_record, overtime_record = get_record(_conversation_id)
    export_excel(original_res, 'original_res.xlsx', path=folder_path)
    export_excel(all_record, 'all_record.xlsx', path=folder_path)
    export_excel(overtime_record, 'overtime_record.xlsx', path=folder_path)
    print(folder_name + '获取成功')
    sleep(2)

# data = json.loads(res)


# # 保存为JSON格式
# with open('all_record_'+recv_id + '.json', 'w', encoding='utf-8') as f:
#     json.dump(all_record, f, ensure_ascii=False, indent=4)
# print("Data saved as JSON.")
