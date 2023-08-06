import datetime as mytime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Consultations


class GenerateConsultation:

    def __init__(self, doctor, patient, service, slot):
        self._created_at = mytime.datetime.now()
        self._deleted_at = None
        self._doctor = doctor.get('id')
        self._start_at = slot.get('start_at')
        self._end_at = self._start_at + mytime.timedelta(minutes=int(service.get('duration')))
        self._external_id = None
        self._external_type = 'slot'
        self._patient = patient.get('id')
        self._pay_source = 'online'
        self._service = service.get('id')
        self._source = 'admin'
        self._status = 'approved'
        self._type = 'online'

    def with_deleted_at(self):
        self._deleted_at = mytime.datetime.now()
        return self

    def with_external_id(self, ex_id):
        self._external_id = ex_id
        return self

    def with_external_type_service_patient(self):
        self._external_type = 'service_patient'

    def with_pay_source_auto_resume(self):
        self._pay_source = 'auto_resume'
        return self

    def with_pay_source_admin(self):
        self._pay_source = 'admin'
        return self

    def with_pay_source_free(self):
        self._pay_source = 'free'
        return self

    def with_pay_source_on_spot(self):
        self._pay_source = 'on_spot'
        return self

    def with_pay_source_trial(self):
        self._pay_source = 'trial'
        return self

    def with_status_canceled(self):
        self._status = 'canceled'
        return self

    def with_status_completed(self):
        self._status = 'completed'
        return self

    def with_status_expired(self):
        self._status = 'expired'
        return self

    def with_status_not_appeared(self):
        self._status = 'not_appeared'
        return self

    def with_status_open(self):
        self._status = 'open'
        return self

    def with_status_pending(self):
        self._status = 'pending'
        return self

    def with_status_wait_payment(self):
        self._status = 'wait_payment'
        return self

    def with_source_doctor(self):
        self._source = 'doctor'
        return self

    def with_source_patient(self):
        self._source = 'patient'
        return self

    def with_source_public_api(self):
        self._source = 'public_api'
        return self

    def with_source_widget_2(self):
        self._source = 'widget_2.0'
        return self

    def with_type_offline(self):
        self._type = 'offline'
        return self

    def with_type_chat(self):
        self._type = 'chat'
        return self

    def generate(self):
        consultation = Consultations(created_at=self._created_at,
                                     updated_at=self._created_at,
                                     doctor=self._doctor,
                                     patient=self._patient,
                                     pay_source=self._pay_source,
                                     source=self._source,
                                     service=self._service,
                                     external_id=self._external_id,
                                     external_type=self._external_type,
                                     status=self._status,
                                     type=self._type,
                                     start_at=self._start_at,
                                     end_at=self._end_at,
                                     deleted_at=self._deleted_at)
        consultation.save()
        return model_to_dict(consultation)
