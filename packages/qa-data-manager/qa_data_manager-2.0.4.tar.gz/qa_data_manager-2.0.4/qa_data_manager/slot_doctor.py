import datetime

from faker import Faker

from qa_data_manager.data_base_model import SlotsDoctors

"""
Генерация слотов.
    Поля:
        * type - Тип слота; Принимает значения both/online/offlien (Онлайн и оффлнай / Онлайн / Оффлайн); По умолчанию both.
        * doctor_id - Идентификатор доктора; Обязательное поле, устанавливается при инициализации класса из параметра doctor.
        * start_at - Дата и время начала слота; Принимает значеиние datetime (Дата и время); По умолчанию текущее время и дата.
        * duration - Длительность слота; Принимает int значение; По умолчанию 5.
        * end_at - Дата и время завершения слота; По умолчанию высчитывается из полей start_at + duration
        * context - Тип обработки слота; Принимает значения default/admin/doctor/integration 
            (По умолванию / Подтверждения администратором / Подтверждение доктором / Интеграция); По умолчанию default.
        * deleted_at - Дата удаления слота; Принимает значения datetime/None (Дата и время / Null); По умолчанию None.
        * count - Количество слотов для генерации; Принимает int значение; По умолчанию 1.
    
    Методы:
        * with_admin_context() - Устанавливает в поле context значение admin.
        * with_doctor_context() - Устанавливает в поле context  значение doctor.
        * with_integration_context() - Устанавливает в поле context значение integration.
        * with_count():
            - Принимает параметр count.
            - Устанавиввает в поле count значение из параметра count.
        * is_deleted() - Устанавливает в поле deleted_at значение datetime (Текущее время и дата).
        * with_online_type() - Устанавливает в поле type значение online.
        * with_offline_type() - Устанавливает в поле type значение offline.
        * with_duration() :
            - Принимает параметр duration.
            - Устанавливает в поле duration значение из параметра duration.
        * generate():
            - Сохраняет объект GenerateSlotDoctor в базу данных.
            - Возвращает список идентификаторов сгенерированных слотов.
"""


class GenerateSlotDoctor:
    __fake = Faker('ru_RU')
    __time_mask = '%Y-%m-%d %H:%M:%S'

    def __init__(self, doctor):
        self._type = 'both'
        self._doctor_id = doctor.get('id')
        self._start_at = datetime.datetime.now()
        self._duration = 5
        self._end_at = self._start_at + datetime.timedelta(minutes=int(self._duration))
        self._context = 'default'
        self._deleted_at = None
        self._count = 1

    def with_admin_context(self):
        self._context = 'admin'
        return self

    def with_doctor_context(self):
        self._context = 'doctor'
        return self

    def with_integration_context(self):
        self._context = 'integration'
        return self

    def with_count(self, count):
        self._count = count
        return self

    def is_deleted(self):
        self._deleted_at = datetime.datetime.now()
        return self

    def with_online_type(self):
        self._type = 'online'
        return self

    def with_offline_type(self):
        self._type = 'offline'
        return self

    def with_duration(self, duration):
        self._duration = duration
        self._end_at = self._start_at + datetime.timedelta(minutes=int(self._duration))
        return self

    def generate(self):
        i = 1
        list_slot_ids = []
        while (i <= self._count):
            slot_doctor = SlotsDoctors(doctor_id=self._doctor_id,
                                       type=self._type,
                                       start_at=self._start_at,
                                       duration=self._duration,
                                       end_at=self._end_at,
                                       context=self._context,
                                       created_at=datetime.datetime.now(),
                                       updated_at=datetime.datetime.now())
            slot_doctor.save()
            list_slot_ids.append(slot_doctor.id)
            i = i + 1
            self._start_at = self._end_at
            self._end_at = self._start_at + datetime.timedelta(minutes=int(self._duration))

        return list_slot_ids
