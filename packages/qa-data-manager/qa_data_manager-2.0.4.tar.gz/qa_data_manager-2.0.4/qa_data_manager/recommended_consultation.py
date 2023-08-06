import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import RecommendedConsultations


class GenerateRecommendedConsultations:
    def __init__(self, doctor, patient):
        self._date_time = datetime.datetime.now() + datetime.timedelta(hours=int('24'))
        self._deleted_at = None
        self._doctor = doctor.get('id')
        self._is_ignored = 0
        self._is_reminded = None
        self._patient = patient.get('id')
        self._previous_slot_patient = None
        self._slot_patient = None

    def with_previous_slot(self, slot_doctor_patient):
        self._previous_slot_patient = slot_doctor_patient.get('id')
        return self

    def with_recommended_time(self, time):
        self._date_time = datetime.datetime.now() + datetime.timedelta(hours=int(time))
        return self

    def with_deleted_at(self):
        self._deleted_at = datetime.datetime.now()
        return self

    def generate(self):
        recommended_consultation = RecommendedConsultations(created_at=datetime.datetime.now(),
                                                            date_time=self._date_time,
                                                            deleted_at=self._deleted_at,
                                                            doctor=self._doctor,
                                                            is_ignored=self._is_ignored,
                                                            is_reminded=self._is_reminded,
                                                            patient=self._patient,
                                                            previous_slot_patient=self._previous_slot_patient,
                                                            slot_patient=self._slot_patient,
                                                            updated_at=datetime.datetime.now())

        recommended_consultation.save()
        return model_to_dict(recommended_consultation)
