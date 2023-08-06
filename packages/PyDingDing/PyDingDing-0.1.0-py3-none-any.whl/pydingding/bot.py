# -*- coding:utf-8 -*-
"""
====================================
@File    :  bot.py
@Author  :  LiuKe
====================================
"""
import base64
import hashlib
import hmac
import json
import time
import urllib.parse

from requests import Request, Session
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_fixed

from .errors import RequestError, VerificationError
from .log import logger


class DingTalkBot:
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret
        self.base_url = "https://oapi.dingtalk.com"
        self.session = Session()

    def _gen_sign(self, t, key):
        secret_enc = key.encode('utf-8')
        string_to_sign = '{}\n{}'.format(t, key)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        return sign


    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(1),
           retry=retry_if_not_exception_type(VerificationError))
    def http_client(self, method, endpoint, header, *args, **kwargs):
        url = f'{self.base_url}{endpoint}'
        req = Request(method, url, headers=header, *args, **kwargs)
        prepped = self.session.prepare_request(req)
        resp = self.session.send(prepped)
        resp_json = resp.json()
        code = resp_json['errcode']
        msg = resp_json['errmsg']

        if code > 0:
            # documentation: https://open.dingtalk.com/document/robots/custom-robot-access
            if code == 310000:
                raise VerificationError(code, msg)
            raise RequestError(code, msg)

        logger.debug(f'requested: url={url} response={resp_json}')

        return resp_json

    def get(self, endpoint, header=None, *args, **kwargs):
        return self.http_client('GET', endpoint, header, *args, **kwargs)

    def post(self, endpoint, header=None, *args, **kwargs):
        return self.http_client('POST', endpoint, header, *args, **kwargs)


    # def upload_image(self, img):
    #     url = "https://open.feishu.cn/open-apis/im/v1/images"
    #     form = {'image_type': 'message', 'image': (open(img, 'rb'))} 
    #     multi_form = MultipartEncoder(form)
    #     token = self.get_access_token()
    #     headers = {
    #         'Authorization': f'Bearer {token}',
    #     }
    #     headers['Content-Type'] = multi_form.content_type
    #     resp = self.post('/im/v1/images', headers=headers, data=multi_form)
    #     print(resp['code'])
    #     image_key = resp['data']['image_key']
    #     logger.debug(f'uploaded image: url={img} image_key={image_key}')
    #     return image_key

    def bot_send(self, msg):
        t = str(round(time.time() * 1000))
        sign = self._gen_sign(t, self.secret)
        header = {"Content-Type": "application/json;charset=utf-8"}
        params = {
            "access_token": self.token,
            "timestamp": t,
            "sign": sign,
        }
        return self.post('/robot/send',header=header,params=params,json=msg)
    
