import uuid
from datetime import datetime

import jwt

from config import Config as cfg

"""
Генератор токена пользователя.
"""


class Jwt_user_toket(object):

    def __init__(self, user):
        prv = ''
        if user == None:
            self._jwt = ''
            return
        if user.get('type') == 'doctor':
            prv = 'e14787aab66688ce06c4712e673e1a1c44f49094'
        if user.get('type') == 'patient':
            prv = '7528956710d1c75b67130d4e4c5c0ee9a0aeb614'
        self._jwt = self.__gererate_token(user.get('id'), prv)
        if user.get('type') == 'admin':
            self._jwt = user.get('api_token')

    def get(self):
        return self._jwt

    def __gererate_token(self, user_id, prv):
        msc = int(datetime.now().timestamp())
        args = {
            "iss": cfg.url + "/api/v3/check-password",
            "iat": msc - 1000,
            "exp": msc + 1000000,
            "nbf": msc - 1000,
            "jti": str(uuid.uuid4()),
            "sub": user_id,
            "prv": prv
        }

        return (jwt.encode(payload=args, key='', algorithm='HS256'))
