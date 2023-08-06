import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Chats

"""
Генерация чата.
    Поля:
        * doctor_id - Идентификатор доктора; Обязательное поле, устанавливается при инициализации класса из параметра doctor.
        * patient_id - Идентификатор пациента; Обязательное поле, устанавливается при инициализации класса из параметра patient.
    
    Метод generate(): 
        -Сохраняет объект GenerateChat в базу данных
        -Возвращает модель таблицы Chats с данными сгенерированного чата.
"""


class GenerateChat:

    def __init__(self, doctor, patient):
        self._doctor_id = doctor.get('id')
        self._patient_id = patient.get('id')

    def generate(self):
        chat = Chats(doctor=self._doctor_id,
                     patient=self._patient_id,
                     created_at=datetime.datetime.now(),
                     updated_at=datetime.datetime.now())
        chat.save()
        return model_to_dict(chat)
