from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import SlotsDoctorsPatientsFile


class GenerateSlotsDoctorsPatientsFile:
    def __init__(self, file, slot_patient):
        self._file = file.get('id')
        self._slot_patient = slot_patient.get('id')

    def generate(self):
        file = SlotsDoctorsPatientsFile(file=self._file,
                                        slot_patient=self._slot_patient)

        file.save()
        return model_to_dict(file)
