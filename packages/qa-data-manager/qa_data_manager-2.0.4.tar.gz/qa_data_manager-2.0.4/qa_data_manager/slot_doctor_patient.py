import datetime
import uuid

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import SlotsDoctorsPatients

"""
Генерация записи в таблицу SlotsDoctorsPatients.
    Поля:
        * batch_id - По умолчанию генерируется аввтоматически.
        * deleted_at - Дата удаления записи; Принимает значения datetime/None (Дата и время / Null); По умолчанию None.
        * is_viewed - ???; Принимает значения 1/0 (True / False); По умолчанию 0.
        * parent - ???; По умолчанию None.
        * patient - Идентификатор пациента; Обязательное поле, устанавливается при инициализации класса из параметра patient.
        * service - Идентификатор тарфиа; Обязательное поле, устанавливается при инициализации класса из параметра service.
        * slot_doctor_id - Идентификатор слота; Обязательное поле, устанавливается при инициализации класса из параметра slot_doctor_id.
        * source - Источник записи; Принимает значения admin/patient/doctor/public-api/widget-2.0 
                            (Админка / Пациент / Доктор / Паблик апи / Виджет 2.0); По умолчанию установлено admin.
        * status - Статус оплаты консультации; Принимает значения wait_payment/canceled/completed/not-appeared/pending; По умолчанию wait_payment.
        * type - Тип слота; Принимает значения both/online/offline (Онлайн и оффлайн / Онлайн / Оффлайн); По умолчанию both.
        * service_patient - Идентификатор записи на консультацию; Принимает значение id/None (Идентификатор записи / Null); По умолчанию None.
        
    Методы:
        * with_offline_type - Устанавливает в поле type значение offline.
        * with_online_type - Устанавливает в поле type значение online.
        * with_patient_source() - Устанавливает в поле source значение patient.
        * with_doctor_source() - Устанавливает в поле source значение doctor.
        * with_public_api_source() - Устанавливает в поле source значение public-api.
        * with_widget_source() - Устанавливает в поле source значение widget-2.0.
        * with_canceled_status() - Устанавливает в поле status значение canceled.
        * with_completed_status() - Устанавливает в поле status значение completed.
        * with_expired_status() - Устанавливает в поле status значение expired.
        * with_not_appeared_status() - Устанавливает в поле status значение not-appeared.
        * with_pending_status() - Устанавливает в поле status значение pending.
        * with_service_patient():
            - Принимает параметр service_patient.
            - Устанавливает в поле service_patient значение из параметра service_patient.
        * generate():
            - Сохраняет объект GenerateSlotDoctorPatient в базу данных.
            - Возвращает модель таблицы SlotsDoctorsPatients с данными сгенерированной записи.
"""


class GenerateSlotDoctorPatient:

    def __init__(self, slot_doctor_id, patient, service):
        self._batch_id = uuid.uuid1()
        self._deleted_at = None
        self._is_viewed = 0
        self._parent = None
        self._patient = patient.get('id')
        self._service = service.get('id')
        self._slot_doctor = slot_doctor_id
        self._source = 'admin'
        self._status = 'wait_payment'
        self._type = 'both'
        self._service_patient = None

    def with_offline_type(self):
        self._type = 'offline'
        return self

    def with_online_type(self):
        self._type = 'online'
        return self

    def with_doctor_source(self):
        self._source = 'doctor'
        return self

    def with_patient_source(self):
        self._source = 'patient'
        return self

    def with_public_api_source(self):
        self._source = 'public-api'
        return self

    def with_widget_source(self):
        self._source = 'widget-2.0'
        return self

    def with_canceled_status(self):
        self._status = 'canceled'
        return self

    def with_completed_status(self):
        self._status = 'completed'
        return self

    def with_expired_status(self):
        self._status = 'expired'
        return self

    def with_not_appeared_status(self):
        self._status = 'not-appeared'
        return self

    def with_pending_status(self):
        self._status = 'pending'
        return self

    def with_service_patient(self, service_patient):
        self._service_patient = service_patient.get('id')
        return self

    def generate(self):
        slot_doctor_patient = SlotsDoctorsPatients(batch_id=self._batch_id,
                                                   created_at=datetime.datetime.now(),
                                                   deleted_at=self._deleted_at,
                                                   is_viewed=self._is_viewed,
                                                   parent=self._parent,
                                                   patient=self._patient,
                                                   service=self._service,
                                                   slot_doctor=self._slot_doctor,
                                                   source=self._source,
                                                   status=self._status,
                                                   type=self._type,
                                                   updated_at=datetime.datetime.now(),
                                                   service_patient_id=self._service_patient)
        slot_doctor_patient.save()
        return model_to_dict(slot_doctor_patient)
