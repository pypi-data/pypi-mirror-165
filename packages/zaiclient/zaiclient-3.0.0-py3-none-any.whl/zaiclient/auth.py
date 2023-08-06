from hashlib import sha256
import hmac
import os
from typing import Type
import requests
from requests.auth import AuthBase
import time

from zaiclient import config

class ZaiHmacAuth(AuthBase):
    '''Z.Ai client-side authentication'''

    def __init__(self, client_id: str=None, secret: str=None):
        if type(client_id) != str:
            raise TypeError('Client ID must be a string value.')
        if type(secret) != str:
            raise TypeError('Secret must be a string value.')
        
        self.__client_id = client_id
        self.__secret = secret

    def __call__(self, request: requests.Request) -> requests.Request:
        timestamp = str(int(time.time()))
        request.headers[config.ZAI_CLIENT_ID_HEADER] = self.__client_id
        request.headers[config.ZAI_UNIX_TIMESTAMP_HEADER] = timestamp
        request.headers[config.ZAI_AUTHORIZATION_HEADER] = f'ZAi {self.__sign(request, timestamp)}'

        return request

    def __sign(self, request, timestamp):
        message = f'/{"/".join(request.url.split("/")[3:])}:{timestamp}'
        signature = hmac.new(
            str.encode(self.__secret, encoding='UTF-8'),
            str.encode(message, encoding='UTF-8'),
            sha256
        ).hexdigest()

        return signature
