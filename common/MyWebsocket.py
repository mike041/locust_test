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
    def on_message(ws, message):
        ms = json.loads(message)
        print('on_message------' + message)
        event = ms['event']
        errCode = ms['errCode']
        data = ms['data']
        if event == 'CreateTextMessage' and errCode == 0:
            ws.SendMessage(data)

    def on_open(ws):
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

    def __init__(self, userId, url, recvID='', groupID='', token=None, on_error=on_error, on_close=on_close,
                 on_open=on_open,
                 on_message=on_message, on_ping=on_ping, on_pong=on_pong):
        self.userId = userId
        self.token = token
        self.recvID = recvID
        self.groupID = groupID
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

    def new_message(self, message, recvID=None, groupID=None):
        if recvID:
            self.recvID = recvID
        if groupID:
            self.groupID = groupID
        self.CreateTextMessage(message)

    def BaseMessage(self, reqFuncName, message):
        t = int(time.time())
        if isinstance(message, dict):
            data = json.dumps(message)
        else:
            data = message
        num = string.ascii_lowercase + string.digits
        operation_id = "".join(random.sample(num, 10)) + str(t) + self.userId
        _message = {"reqFuncName": reqFuncName,
                    "operationID": operation_id,
                    "userID": self.userId,
                    "data": str(data)}
        print("BaseMessage--------" + reqFuncName + json.dumps(_message))
        return json.dumps(_message)

    def CreateTextMessage(self, message):
        _message = self.BaseMessage('CreateTextMessage', message)
        self.send(_message)

    def SendMessage(self, message):
        data_json = {
            "recvID": self.recvID,
            "groupID": self.groupID,
            "offlinePushInfo": "{\"title\":\"你收到一条新消息\",\"desc\":\"\",\"ex\":\"\",\"iOSPushSound\":\"+1\",\"iOSBadgeCount\":true}",
            "message": message
        }

        _message = self.BaseMessage('SendMessage', json.dumps(data_json))
        self.send(_message)


# 手动交互发消息
# def create_message(ws):
#     while True:
#         time.sleep(1)
#         message = ws.CreateTextMessage(reqFuncName='CreateTextMessage', userID=ws.userId, data=input('发送的消息是：'))
#         ws.send(message)


# 自动发消息
def auto_send_meaasge(ws: MindWebSocket):
    for i in range(2):
        print('==================第四步')
        time.sleep(2)
        t = int(time.time())
        num = string.ascii_lowercase + string.digits
        message = "".join(random.sample(num, 10)) + str(t) + ws.userId
        ws.new_message(message=message)
    ws.new_message(message='结束发言')


if __name__ == '__main__':
    path = 'wss://premind.im30.net'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVSUQiOiI4cDV0dHdjeXUzZnN6Z2ppXzZmOHVvZ2JvaGpiZHprZjMiLCJQbGF0Zm9ybSI6IldlYiIsImV4cCI6MTk4MzQyMDcxMiwibmJmIjoxNjY4MDYwNDEyLCJpYXQiOjE2NjgwNjA3MTJ9.QJJJ2zNW1TC_DDYgItxnfki7RbRbA0eqqo9cWXscTDE'
    userId = '8p5ttwcyu3fszgji_6f8uogbohjbdzkf3'
    group_id = '367694aea403361e2cd42377fd2bcd29'
    receive_id = ''
    websocket_client = MindWebSocket(userId,
                                     url='wss://premind.im30.net/ws/web?sendID=8p5ttwcyu3fszgji_6f8uogbohjbdzkf3&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVSUQiOiI4cDV0dHdjeXUzZnN6Z2ppXzZmOHVvZ2JvaGpiZHprZjMiLCJQbGF0Zm9ybSI6IldlYiIsImV4cCI6MTk4MzQyMDcxMiwibmJmIjoxNjY4MDYwNDEyLCJpYXQiOjE2NjgwNjA3MTJ9.QJJJ2zNW1TC_DDYgItxnfki7RbRbA0eqqo9cWXscTDE&platformID=5',
                                     groupID=group_id,
                                     recvID=receive_id)
    websocket_client.run_forever()
