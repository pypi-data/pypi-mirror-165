import datetime as mytime

from faker import Faker
from playhouse.shortcuts import model_to_dict

from qa_data_manager.bind_clinic_user import BindClinicUser
from qa_data_manager.data_base_model import Users

"""
Генерация пользователя.
    Поля:
        * type - Тип пользователя; Принимает значения doctor/patient; По умолчанию doctor.
        * self_appointment - Доступна самостоятельная  запись; Принимает значения 1/0 (True / False); По умолчанию 0.
        * has_primary_acceptance - Доступен первичный прием; Принимает значения 1/0 (True / False); По умолчанию 0.
        * activated_at - Дата активации пользователя; Принимает значениия datetime/None (Датаактивации / Null); По умолчанию None.
        * deleted_at - Дата удаления пользователя; Принимает значения datetime/None (Дата_удаления / Null); По умолчанию None.
        * type_chat - Тип чата; Принимает значения free/paid (Открытый чат / Платный чат); По умолчанию free.
        * clinic - Клиника; Принимает значение id клиники; По умолчанию 14.
        * is_showcase - Отображать на витрине; Принимает значения 1/0 (True / False); По умолчанию 1.
        * dead_zone - Мертвая зона; Принимает значения int/None (Число / Null); По умолчанию None.
        
    Методы:
        * doctor() - Устанавливает в поле type значение doctor.
        * patient() - Устанавливает в поле type значение patient.
        * with_self_appointment() - Устанавливает в поле self_appointment значение 1 (True).
        * with_primary_acceptance() - Устанавливает в поле has_primary_acceptance значение 1 (True).
        * with_paid_chat() - Устанавливает в поле type_chat значение paid (Платный).
        * is_showcase_false() - Устанавливает в поле is_showcase значение 0 (False).
        * is_activated() - Устанавливает в поле activated_at значение datetime (Текущая дата и время).
        * is_deleted() - Устанавливает в поле deleted_at значение datetime (Текущая дата и время).
        * with_clinic():
         - Принимает параметр clinic. 
         - Устанавливает в поле clinic значение из параметра clinic.
        * generate():
            - Сохраняет объект GenerateUser в базу данных.
            - Возвращает модель таблицы Users с данными сгенерированного пользователя.
"""


class GenerateUser:
    fake = Faker('ru_RU')

    # При инициализации класса устанавливаются значения полей по умолчанию
    def __init__(self):
        self._type = 'doctor'
        self._self_appointment = 0
        self._has_primary_acceptance = 0
        self._activatied_at = None
        self._deleted_at = None
        self._type_chat = 'free'
        self._clinic = 14
        self._is_showcase = 1
        self._dead_zone = None

    def patient(self):
        self._type = 'patient'
        return self

    def doctor(self):
        self._type = 'doctor'
        return self

    def with_self_appointment(self):
        self._self_appointment = 1
        return self

    def with_primary_acceptance(self):
        self._has_primary_acceptance = 1
        return self

    def with_paid_chat(self):
        self._type_chat = 'paid'
        return self

    def is_showcase_false(self):
        self._is_showcase = 0
        return self

    def is_activated(self):
        self._activatied_at = mytime.datetime.now()
        return self

    def is_deleted(self):
        self._deleted_at = mytime.datetime.now()
        return self

    def with_clinic(self, clinic):
        self._clinic = clinic.get('id')
        return self

    def with_dead_zone(self, value):
        self._dead_zone = value
        return self

    def generate(self):
        user = Users(activated_at=self._activatied_at,
                     avatar=self.fake.image_url(width=None, height=None),
                     created_at=mytime.datetime.now(),
                     date_of_birth=self.fake.date(pattern="%Y-%m-%d", end_datetime=None),
                     email=self.fake.email(),
                     full_name=self.fake.name(),
                     gender='male',
                     has_primary_acceptance=self._has_primary_acceptance,
                     hash="XRJI",
                     is_showcase=self._is_showcase,
                     is_test=0,
                     password="$2y$12$F02YDfRJLKD/nuNVhIefY.Ux1lkbd8jYdNmtH3c22F/o/8eQNZwzO",
                     phone=self.fake.numerify(text='+0%%%%%%%%%%'),
                     remember_token="blUSTapXajDs1BNFfLOKPrSumVExvthjaE80cP9qqZpA6l54b7vwKXkqbg6W",
                     save_video_at=0,
                     self_appointment=self._self_appointment,
                     send_email=1,
                     send_sms=1,
                     silence_activated_at=0,
                     source='admin',
                     type=self._type,
                     type_chat=self._type_chat,
                     updated_at=mytime.datetime.now(),
                     deleted_at=self._deleted_at,
                     dead_zone=self._dead_zone)
        user.save()
        BindClinicUser(model_to_dict(user)).with_clinic(self._clinic).generate()
        return model_to_dict(user)
