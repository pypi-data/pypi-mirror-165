from config import Config as conf
from qa_data_manager.data_base_model import database

"""
Инициализация база данных.
    Метод connection():
        - Инициализирует подключание к базе данных.
        Принимает параметры:
            * db_host - Хост базы данных.
            * db_name - Имя базы данных.
            * db_port - Порт базы данных.
            * user_name - Пользователь базы данных.
            * user_password - Пароль пользльвателья базы данных.
            * base_url - Эндпоинт для доступа к апи.
    
    Комментарий:
        * Необходимо инициализировать перед работой с классами библиотеки.
"""


class DBManager:

    @staticmethod
    def connection(db_host, db_name, db_port, user_name, user_password, base_url):
        database.init(db_name, host=db_host, port=db_port, user=user_name, password=user_password)
        conf.url = base_url
