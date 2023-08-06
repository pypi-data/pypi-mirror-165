import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Conclusions


class GenerateConclusions:

    def __init__(self, appoint, serv_pat):
        self._appointment = appoint.get('id')
        self._created_at = datetime.datetime.now()
        self._service_patient = serv_pat.get('id')
        self._text = 'text for test'
        self._updated_at = self._created_at

    def with_text(self, my_text):
        self._text = my_text
        return self

    def generate(self):
        conclusion = Conclusions(appointment=self._appointment,
                                 created_at=datetime.datetime.now(),
                                 service_patient=self._service_patient,
                                 text=self._text,
                                 updated_at=datetime.datetime.now())

        conclusion.save()
        return model_to_dict(conclusion)
