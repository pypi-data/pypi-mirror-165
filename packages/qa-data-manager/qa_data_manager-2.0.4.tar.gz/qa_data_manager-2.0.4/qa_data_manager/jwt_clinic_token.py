from datetime import datetime

import jwt

"""
Генератор токена клиники.
"""

class Jwt_clinic_toket(object):

    def __init__(self, client_key, client_secret):
        self._client_key = client_key
        self._client_secret = client_secret
        self._jwt = self.__gererate_token()

    def get(self):
        return self._jwt

    def __gererate_token(self):
        msc = int(datetime.now().timestamp())

        args = {
            "iat": msc - 10000,
            "exp": msc + 300000000000,
            "sub": self._client_key,
        }

        return (jwt.encode(payload=args, key=self._client_secret, algorithm='HS256')).decode("utf-8")
