import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import DoctorPatient

"""
Связь доктора с пациентом.
    Поля:
        * doctor_id - Идентификатор доктора; Обязательное поле, устанавливается при инициализации класса из параметра doctor.
        * patient_id - Идентификатор пациента; Обязательное поле, устанавливается при инициализации класса из параметра patient.
    
    Метод generate():
        - Сохраняет объект BindDoctorPatient в базу данных.
        - Возвращает модель таблицы DoctorPatient с данными сгенерированной связи.
"""


class BindDoctorPatient:

    def __init__(self, doctor, patient):
        self._doctor_id = doctor.get('id')
        self._patient_id = patient.get('id')

    def generate(self):
        doctor_patient = DoctorPatient(confirm_appointment=0,
                                       created_at=datetime.datetime.now(),
                                       doctor=self._doctor_id,
                                       doctor_new=1,
                                       message='hello user',
                                       patient=self._patient_id,
                                       patient_new=1,
                                       source='admin',
                                       updated_at=datetime.datetime.now())
        doctor_patient.save()
        return model_to_dict(doctor_patient)
