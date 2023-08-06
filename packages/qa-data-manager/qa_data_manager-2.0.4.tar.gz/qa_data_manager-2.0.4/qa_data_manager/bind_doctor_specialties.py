import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import DoctorSpecialties

"""
Установка специальности доктору.
    Поля:
        * doctor_id - Идентификатор доктора; Обязательное поле, устанавливается при инициализации класса из параметра doctor.
        * specialty - Ключ специальности; По умолчанию pediatrician.
        
    Методы:
        * with_specialty():
            - Принимает параметр spec.
            - Устанавливает в поле specialty значение ключа специальности из параметра spec.
            
        * generate():
            - Сохраняет объект BindDoctorSpecialties в базу данных.
            - Возвращает модель таблицы DoctorSpecialties с данными сгенерированной связи.
"""


class BindDoctorSpecialties:

    def __init__(self, doctor):
        self._doctor_id = doctor.get('id')
        self._specialty = 'pediatrician'

    def with_specialty(self, spec):
        self._specialty = spec
        return self

    def generate(self):
        doc_spec = DoctorSpecialties(doctor_id=self._doctor_id,
                                     specialty=self._specialty,
                                     created_at=datetime.datetime.now(),
                                     updated_at=datetime.datetime.now())
        doc_spec.save()
        return model_to_dict(doc_spec)
