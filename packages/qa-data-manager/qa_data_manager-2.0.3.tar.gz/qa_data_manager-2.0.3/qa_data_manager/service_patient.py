import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import ServicesPatients

"""
Генерация записи в таблицу ServicesPatients.
    Поля:
        * deleted_at - Дата удаления; Принимает значение datetime/None (Дата и время / Null); По умолчанию None.
        * external_id - ???
        * invoice_id - Идентификатор платежа; Принимает значение id платежа/None (id / Null); По умолчанию None.
        * is_finished - Консультация завершена; Принимает значения 1/0 (True / False); По умолчанию 0 (False).
        * patient - Идентификатор пациента; Обязательное поле, устанавливается при инициализации класса из параметра patient.
        * service - Издентификатор тарифа; Обязательное поле, устанавливается при инициализации класса из параметра service.
        * source - Источник записи; Принимает значения admin/patient/doctor/public-api/widget-2.0 
                            (Админка / Пациент / Доктор / Паблик апи / Виджет 2.0); По умолчанию установлено admin.
        * start_at - Время начала консультации; Принимает значение datetime/None (Дата и время / Null); По умолчанию генерируется текущее время и дата.
        * end_at - Время окончания консультации; Принимает значение datetime/None (Дата и время / Null); По умолчанию None.
        * subscription - ???
        * type - Тип тарифа; Принимает значения chat/av/offline (Чат / Видео / Очный); По умолчанию chat.
        
    Методы:
        * with_invoice():
            - Принимает параметр invoice_id.
            - Устанавливает в поле invoice_id значение из параметра invoice_id.
        * with_external():
            - Принимает параметр external_id.
            - Устанавливает в поле external_id значение из параметра external_id.
        * is_finished() - Устанавливает в поле is_finished значение 1 (True).
        * with_patient_source() - Устанавливает в поле source значение patient.
        * with_doctor_source() - Устанавливает в поле source значение doctor.
        * with_public_api_source() - Устанавливает в поле source значение public-api.
        * with_widget_source() - Устанавливает в поле source значение widget-2.0.
        * with_online_type() - Устанавливает в поле type значение av.
        * with_offline_type() - Устанавливает в поле type значение offline.
        * generate():
            - Сохраняет объект GenerateServicePatient в базу данных.
            - Возвращает модель таблицы ServicesPatients с данными сгенерированной записи.
"""


class GenerateServicePatient:

    def __init__(self, service, patient):
        self._deleted_at = None
        self._external_id = None
        self._invoice = None
        self._is_finished = 0
        self._patient = patient.get('id')
        self._service = service.get('id')
        self._source = 'admin'
        self._start_at = datetime.datetime.now()
        self._end_at = None
        self._subscription = None
        self._type = 'chat'

    def with_invoice(self, invoice_id):
        self._invoice = invoice_id
        return self

    def with_external(self, external_id):
        self._external_id = external_id
        return self

    def is_finished(self):
        self._is_finished = 1
        return self

    def with_patient_source(self):
        self._source = 'patient'
        return self

    def with_doctor_source(self):
        self._source = 'doctor'
        return self

    def with_public_api_source(self):
        self._source = 'public-api'
        return self

    def with_widget_source(self):
        self._source = 'widget-2.0'
        return self

    def with_online_type(self):
        self._type = 'av'
        return self

    def with_offline_type(self):
        self._type = 'offline'
        return self

    def generate(self):
        service_patient = ServicesPatients(created_at=datetime.datetime.now(),
                                           updated_at=datetime.datetime.now(),
                                           deleted_at=self._deleted_at,
                                           external_id=self._external_id,
                                           invoice=self._invoice,
                                           is_finished=self._is_finished,
                                           patient=self._patient,
                                           service=self._service,
                                           source=self._source,
                                           start_at=self._start_at,
                                           end_at=self._end_at,
                                           subscription=self._subscription,
                                           type=self._type)
        service_patient.save()
        return model_to_dict(service_patient)
