from qa_data_manager.jwt_clinic_token import Jwt_clinic_toket

"""
Генерация токена клиники.
    Метод get_token():
        - Принимает параметры client_key и client_secret.
        - Возввращает сгенерированный токен клиники.
"""


class GenerateClinicToken:

    def get_token(self, client_key, client_secret):
        return Jwt_clinic_toket(client_key, client_secret).get()
