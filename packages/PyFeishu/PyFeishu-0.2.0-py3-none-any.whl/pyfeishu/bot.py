# -*- coding:utf-8 -*-
"""
====================================
@File    :  bot.py
@Author  :  LiuKe
====================================
"""

from datetime import timedelta
import json
from cachetools import TTLCache, keys
from requests import Request, Session
from requests_toolbelt import MultipartEncoder
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from .errors import NoPermissionError, RequestError, TokenExpiredError
from .log import logger


class FeishuBot:
    def __init__(self, app_id,
                 app_secret,
                 base_url='https://open.feishu.cn/open-apis',
                 token_ttl=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = base_url
        self.token_cache = TTLCache(1, token_ttl or timedelta(minutes=100).seconds)

    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(1),
           retry=retry_if_exception_type(TokenExpiredError))
    def http_client(self, method, endpoint, headers, *args, **kwargs):
        url = f'{self.base_url}{endpoint}'

        s = Session()
        req = Request(method, url, headers=headers, *args, **kwargs)
        prepped = s.prepare_request(req)
        resp = s.send(prepped)
        resp_json = resp.json()
        code = resp_json['code']
        msg = resp_json['msg']

        if code > 0:
            # documentation: https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN
            if code == 99991663:
                self.token_cache.clear()
                raise TokenExpiredError(code, msg)
            if code == 99991672:
                raise NoPermissionError(code, msg)
            raise RequestError(code, msg)

        logger.debug(f'requested: url={url} response={resp_json}')

        return resp_json

    def get(self, endpoint, headers=None, *args, **kwargs):
        return self.http_client('GET', endpoint, headers, *args, **kwargs)

    def post(self, endpoint, headers=None, *args, **kwargs):
        return self.http_client('POST', endpoint, headers, *args, **kwargs)

    def get_access_token(self):
        cached_token = self.token_cache.get(keys.hashkey(self))
        if cached_token:
            return cached_token
        url = f'/auth/v3/tenant_access_token/internal/'
        resp = self.post(url,
                         json={
                                'app_id': self.app_id,
                                'app_secret': self.app_secret
                               })
        token = resp['tenant_access_token']
        self.token_cache[keys.hashkey(self)] = token

        return token

    def get_group(self):
        url = f'/im/v1/chats'
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
        }
        resp = self.get(url,headers=headers)
        return resp


    def upload_image(self, img):
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        form = {'image_type': 'message', 'image': (open(img, 'rb'))} 
        multi_form = MultipartEncoder(form)
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
        }
        headers['Content-Type'] = multi_form.content_type
        resp = self.post('/im/v1/images', headers=headers, data=multi_form)
        print(resp['code'])
        image_key = resp['data']['image_key']
        logger.debug(f'uploaded image: url={img} image_key={image_key}')
        return image_key

    def send_msg(self, msg, recv_id, type='text', recv_id_type='chat_id'):
        token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json; charset=utf-8',
        }
        params = {"receive_id_type": recv_id_type}
        payload = {
            "receive_id": recv_id,
            "content": json.dumps(msg),
            "msg_type": type,
        }
        return self.post('/im/v1/messages',headers=headers,params=params,json=payload)
    
