from qa_data_manager.jwt_user_token import Jwt_user_toket

"""
Генерация токена пользовавтеля.
    Метод get_token():
        - Принимает параметр user.
        - Возввращает сгенерированный токен пользователя.
"""


class GenerateUserToken:

    def get_token(self, user):
        return Jwt_user_toket(user).get()
