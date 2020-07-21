import requests
from edu_api.settings import constants


class Message(object):

    def __init__(self, api_key):
        # 账号唯一标识
        self.api_key = api_key
        # 单条短信发送接口
        self.single_send_url = constants.SINGLE_SEND_URL

    def send_message(self, phone, code):
        """
        短信发送的实现
        :param phone: 前端传递的手机号
        :param code: 随机验证码
        :return:
        """
        params = {
            "apikey": self.api_key,
            'mobile': phone,
            'text': "【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        # 可以发送http请求
        req = requests.post(self.single_send_url, data=params)
        print(req)


if __name__ == '__main__':
    message = Message(constants.API_KEY)
    message.send_message("13130951173", "123456")
