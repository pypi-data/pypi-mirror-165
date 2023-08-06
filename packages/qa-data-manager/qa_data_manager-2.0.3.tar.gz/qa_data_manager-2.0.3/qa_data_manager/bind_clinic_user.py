import datetime

from qa_data_manager.data_base_model import ClinicUser

"""
Связь пользователя с клиникой.
    Поля:
        * clinic_id - Индентификатор клиники; По умолчанию 14.
        * user_id - Индентификатор пользовавтелья; Обязательное поле, устанавливается при инциализации класса из параметра user.
        * type - Тип пользователя; Устанавливается при инициализации класса из параметра user.
        
    Методы:
        * with_clinic():
            - Принимает параметр clinic_id.
            - Устанавливает в поле clinic_id значение идентификатора клиники из параметра clinic_id.
        * generate():
            - Сохраняет объект BindClinicUser в базу данных.
            - Возвращает модель таблицы ClinicUser с данными сгенерированной связи.
"""


class BindClinicUser:

    def __init__(self, user):
        self._clinic_id = 14
        self._user_id = user.get('id')
        self._type = user.get('type')

    def with_clinic(self, clinic_id):
        self._clinic_id = clinic_id
        return self

    def generate(self):
        clinic_user = ClinicUser(clinic=self._clinic_id,
                                 created_at=datetime.datetime.now(),
                                 type=self._type,
                                 updated_at=datetime.datetime.now(),
                                 user=self._user_id)
        clinic_user.save()
        return clinic_user
