import datetime as mytime

from faker import Faker
from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Services

"""
Генерация тарифа.
    Поля:
        * doctor_id - Идентификатор доктора; Обязательное поле, устанавливается при инициализации класса из параметра doctor.
        * is_active - Активный тариф; Принимает значения 1/0 (True / False); По умолчанию 0.
        * type_of_service - Тип тарифа; Принимает значения av/chat/offline (Видео / Чат / Очный); По умолнчаию av.
        * price - Стоимость тарифа; Принимает int значение; По умолчаниию 10.
        * duration - Длительность тарифа; Принимает int значение; По умолнчаию 5.
        * is_hidden - Скрытый тариф; Принимает значения 1/0 (True / False); По умолчанию 0.
        * can_close - Закрытие врачем; Приинимает значения 1/0 (True/ False); По умолчанию 0.
        * is_auto_resume - Автопродление; Принимает значения 1/0 (True / False); По умолчанию 0.
        * is_trial - Триальный период; Принимает значения 1/0 (True / False); По умолчанию 0.
        * is_default - Тариф по дефолту; Принимает значения 1/0 (True / False); По умолчанию 0.
        * name - Название тарифа; Принимает string значение; По умолчанию генерируется рандомное название.
    
    Методы:
        * with_chat_service_type() - Устанавливает в поле type_of_service значение chat.
        * with_offline_service_type() - Устанавливает в поле type_of_service значение offline.
        * is_active() - Устанавливает в поле is_active значение 1 (True).
        * is_can_close() - Устанавливает в поле can_close значение 1 (True).
        * with_duration():
            - Принимает параметр duration.
            - Устанавливает в поле duration значение из параметра duration.
        * is_hidden() - Устанавливает в поле is_hidden значение 1 (True).
        * with_price():
            - Принимает параметр price.
            - Устанавливает в поле price значение из параметра price.
        * is_trial() - Устанавливает в поле is_trial значение 1 (True).
        * is_auto_resume() - Устанавливает в поле is_auto_resume значение 1 (True).
        * is_default() - Устанавливает в поле is_default значение 1 (True).
        * generate():
            - Сохраняет объект GenerateService в базу данных.
            - Возвращает модель таблицы Services с данными сгенерированного тарифа.
"""


class GenerateService:
    __fake = Faker('ru_RU')

    def __init__(self, doctor):
        self._doctor_id = doctor.get('id')
        self._is_active = 0
        self._type_of_service = 'av'
        self._price = 10
        self._duration = 5
        self._is_hidden = 0
        self._can_close = 0
        self._is_auto_resume = 0
        self._is_trial = 0
        self._is_default = 0
        self._name = 'tarif' + self.__fake.pystr()

    def with_chat_service_type(self):
        self._type_of_service = 'chat'
        return self

    def with_offline_service_type(self):
        self._type_of_service = 'offline'
        return self

    def is_active(self):
        self._is_active = 1
        return self

    def is_can_close(self):
        self._can_close = 1
        return self

    def with_duration(self, duration):
        self._duration = duration
        return self

    def is_hidden(self):
        self._is_hidden = 1

    def with_price(self, price):
        self._price = price
        return self

    def is_trial(self):
        self._is_trial = 1
        return self

    def is_auto_resume(self):
        self._is_auto_resume = 1
        return self

    def is_default(self):
        self._is_default = 1
        return self

    def generate(self):
        service = Services(active=self._is_active,
                           can_close=self._can_close,
                           created_at=mytime.datetime.now(),
                           description='test tarif description',
                           doctor=self._doctor_id,
                           duration=self._duration,
                           is_auto_resume=self._is_auto_resume,
                           is_default=self._is_default,
                           is_hidden=self._is_hidden,
                           is_trial=self._is_trial,
                           name=self._name,
                           price=self._price,
                           service_type=self._type_of_service,
                           updated_at=mytime.datetime.now())
        service.save()
        return model_to_dict(service)
