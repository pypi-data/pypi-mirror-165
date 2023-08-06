# -*- coding:utf-8 -*-
"""
====================================
@File    :  bot.py
@Author  :  LiuKe
====================================
"""
import base64
import hashlib

from requests import Request, Session
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt,wait_fixed

from .errors import InvalidKeyError, RequestError
from .log import logger


class QyWechatBot:
    def __init__(self, 
                 key,
                 base_url='https://qyapi.weixin.qq.com'):
        self.key = key
        self.base_url = base_url
        self.s = Session()

    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(1),
           retry=retry_if_not_exception_type(InvalidKeyError))
    def http_client(self, method, endpoint, headers, *args, **kwargs):
        url = f'{self.base_url}{endpoint}'
        req = Request(method, url, headers=headers, *args, **kwargs)
        prepped = self.s.prepare_request(req)
        resp = self.s.send(prepped)
        resp_json = resp.json()
        code = resp_json['errcode']
        msg = resp_json['errmsg']

        if code > 0:
            # documentation: https://developer.work.weixin.qq.com/document/path/90475
            if code == 40058:
                raise InvalidKeyError(code, msg)
            raise RequestError(code, msg)

        logger.debug(f'requested: url={url} response={resp_json}')

        return resp_json

    def get(self, endpoint, headers=None, *args, **kwargs):
        return self.http_client('GET', endpoint, headers, *args, **kwargs)

    def post(self, endpoint, headers=None, *args, **kwargs):
        return self.http_client('POST', endpoint, headers, *args, **kwargs)

    def upload_file(self, file):
        params = {"key": self.key, "type": "file"}
        file = {"file": open(file, "rb")}
        resp = self.post('/cgi-bin/webhook/upload_media', params=params, files=file)
        media_id = resp['media_id']
        logger.debug(f'uploaded file: url={file} media_id={media_id}')
        return media_id

    def send_msg(self, msg):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        params = {"key": self.key}
        return self.post('/cgi-bin/webhook/send', headers=headers,params=params,json=msg)

    def img_msg(self, img):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        params = {"key": self.key}
        with open(img, 'rb') as f:
            fd = f.read()
            b64_str = base64.b64encode(fd).decode('utf-8')
            md5 = hashlib.md5()
            md5.update(fd)
            md5_str = md5.hexdigest()

        payload = {
            "msgtype": "image",
            "image": {
                "base64": b64_str,
		        "md5": md5_str
                }
        }
        return self.post('/cgi-bin/webhook/send', headers=headers,params=params,json=payload)

    
    
