"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: MyWebsocket
@Site:
@time: 2022.10.27
"""
import json
import random
import string
import threading
import time

from websocket import WebSocketApp


class MindWebSocket(WebSocketApp):
    to_send_message_dict = {}

    def on_message(ws, message):
        ms = json.loads(message)
        event = ms['event']
        errCode = ms['errCode']
        operation_id = ms['operationID']
        print('on_message------' + message)
        data = ms['data']
        # 创建消息成功，去发送消息
        if event == 'CreateTextMessage' and ws.to_send_message_dict[operation_id] and errCode == 0:
            print('on_message------' + message)
            ws.SendMessage(data, groupID=ws.group_id)
            ws.to_send_message_dict.pop(operation_id)

    def on_open(ws):
        pass
        th = threading.Thread(name='t1', target=auto_send_meaasge, args=(ws,))
        th.start()

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print('已关闭')

    # 心跳检查,保持websocket链接状态
    def on_ping(ws, message):
        print("Got a Ping:")
        print(message)

    def on_pong(ws, message):
        print("Got a Pong:")
        print(message)

    def __init__(self, user_id, url, group_id=None, on_error=on_error, on_close=on_close, on_open=on_open,
                 on_message=on_message, on_ping=on_ping, on_pong=on_pong):
        self.user_id = user_id
        self.group_id = group_id
        # self.token = token
        super(MindWebSocket, self).__init__(url,
                                            header=None,
                                            on_open=on_open,
                                            on_message=on_message,
                                            on_error=on_error,
                                            on_close=on_close,
                                            on_ping=on_ping, on_pong=on_pong,
                                            on_cont_message=None,
                                            keep_running=True,
                                            get_mask_key=None,
                                            cookie=None,
                                            subprotocols=None,
                                            on_data=None,
                                            socket=None)

    def BaseMessage(self, reqFuncName, data):  # 发送完消息后将 操作id返回
        t = int(time.time())
        if isinstance(data, dict):
            data = json.dumps(data)
        num = string.ascii_lowercase + string.digits
        operation_id = "".join(random.sample(num, 10)) + str(t) + self.user_id
        _message = {"reqFuncName": reqFuncName,
                    "operationID": operation_id,
                    "userID": self.user_id,
                    "data": str(data)}
        return operation_id, json.dumps(_message)

    def CreateTextMessage(self, reqFuncName='CreateTextMessage', data=None):
        operation_id, message = self.BaseMessage(reqFuncName, data)
        self.send(message)
        # 创建文本信息并将操作id存下来
        self.to_send_message_dict[operation_id] = operation_id

    def SendMessage(self, message, recvID='', groupID=None, ):
        data_json = {
            "recvID": recvID,
            "groupID": groupID,
            "offlinePushInfo": "{\"title\":\"你收到一条新消息\",\"desc\":\"\",\"ex\":\"\",\"iOSPushSound\":\"+1\",\"iOSBadgeCount\":true}",
            "message": message
        }

        operation_id, message = self.BaseMessage('SendMessage', json.dumps(data_json))
        self.send(message)
        # 创建文本信息并将操作id存下来
        self.to_send_message_dict[operation_id] = operation_id

    # # 手动交互发消息
    # def create_message(ws):
    #     while True:
    #         time.sleep(1)
    #         message = ws.structure_message(reqFuncName='CreateTextMessage', userID=ws.user_id, data=input('发送的消息是：'))
    #         ws.send(message)
    #
    # 自动发消息


def auto_send_meaasge(ws: MindWebSocket):
    ws.CreateTextMessage(reqFuncName='CreateTextMessage', data='发言开始')
    for i in range(random.randint(1, 10)):
        time.sleep(random.randint(1, 10))
        num = string.ascii_letters + string.digits
        rand = "".join(random.sample(num, 10))
        ws.CreateTextMessage(reqFuncName='CreateTextMessage', data=rand)
    ws.CreateTextMessage(reqFuncName='CreateTextMessage', data='发言结束')
    ws.close()


if __name__ == '__main__':
    domain = 'mind.im30.lan'
    path = 'wss://' + domain
    user = 15902379217
    user_id = '4g839u4dff8qdpzo_f58xiaus7frnmqfz'
    group_id = '411809625'
    receive_id = ''
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVSUQiOiI0ZzgzOXU0ZGZmOHFkcHpvX2Y1OHhpYXVzN2Zybm1xZnoiLCJQbGF0Zm9ybSI6IldlYiIsImV4cCI6MTk4MjU1OTUwOCwibmJmIjoxNjY3MTk5MjA4LCJpYXQiOjE2NjcxOTk1MDh9.Ph0fu2xJ2xbpkRPXlfdhQv_3myi9YrqWvAht0Sdr7E8'

    websocket_client = MindWebSocket('4g839u4dff8qdpzo_f58xiaus7frnmqfz',
                                     url='ws://10.2.4.100:30000/?sendID=4g839u4dff8qdpzo_f58xiaus7frnmqfz&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVSUQiOiI0ZzgzOXU0ZGZmOHFkcHpvX2Y1OHhpYXVzN2Zybm1xZnoiLCJQbGF0Zm9ybSI6IldlYiIsImV4cCI6MTk4MjU1OTUwOCwibmJmIjoxNjY3MTk5MjA4LCJpYXQiOjE2NjcxOTk1MDh9.Ph0fu2xJ2xbpkRPXlfdhQv_3myi9YrqWvAht0Sdr7E8&platformID=5',
                                     group_id=group_id)
    websocket_client.run_forever()
