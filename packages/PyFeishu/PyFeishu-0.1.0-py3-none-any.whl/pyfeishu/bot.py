from datetime import timedelta

from cachetools import TTLCache, keys
from requests import Request, Session
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from .errors import RequestError, TokenExpiredError,NoPermissionError
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
    def http_client(self, method, endpoint, *args, **kwargs):
        url = f'{self.base_url}{endpoint}'
        no_auth = kwargs.pop('no_auth', False)
        if no_auth:
            headers = kwargs.pop('headers', {})
        else:
            token = self.get_access_token()
            headers = {
                'Authorization': f'Bearer {token}',
                **kwargs.pop('headers', {})
            }
        s = Session()
        req = Request(method, url, *args, headers=headers, **kwargs)
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

    def get(self, endpoint, *args, **kwargs):
        return self.http_client('GET', endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self.http_client('POST', endpoint, *args, **kwargs)

    def get_access_token(self):
        cached_token = self.token_cache.get(keys.hashkey(self))
        if cached_token:
            return cached_token
        url = f'/auth/v3/tenant_access_token/internal/'
        resp = self.post(url,
                         no_auth=True,
                         json={
                                'app_id': self.app_id,
                                'app_secret': self.app_secret
                               })
        token = resp['tenant_access_token']
        self.token_cache[keys.hashkey(self)] = token

        return token

    def get_groups(self):
        resp = self.get('/chat/v4/list')
        return resp['data']['groups']

    def send_to_groups(self, msg_type, content=None, card=None, **kwargs):
        groups = kwargs.get('groups')
        if groups is None:
            detailed_groups = self.get_groups()
            groups = [g['chat_id'] for g in detailed_groups]
        elif isinstance(groups, str):
            # single chat_id
            groups = [groups]
        result = []
        for g in groups:
            payload = {
                'chat_id': g,
                'msg_type': msg_type,
            }
            if card is not None:
                payload['card'] = card
                payload['update_multi'] = kwargs['is_shared']
            else:
                payload['content'] = content
            res = self.post('/message/v4/send/', json=payload)
            result.append(res)

        logger.debug(f'Sent {msg_type}={content} to {[g for g in groups]}')

        return result

    def send_text(self, text: str, groups=None):
        """
        Send plain text
        """
        return self.send_to_groups('text', {'text': text}, groups=groups)

    def upload_image(self, img):
        """
        Upload image of the given url
        """
        # files = [('image',('tu.png',open('tup.png','rb'))),]
        b = open(img,'rb')
        resp = self.post('/im/v1/images',
                        data={
                            'image_type': 'message',
                            'image': b})
        print("0"*100)
        print(resp['code'])
        image_key = resp['data']['image_key']
        logger.debug(f'uploaded image: url={img} image_key={image_key}')
        return image_key

    def send_image(self, img, groups=None):
        """
        Send image
        """
        image_key = self.upload_image(img)
        return self.send_to_groups('image', {'image_key': image_key}, groups=groups)



if __name__ == '__main__':
    pass
