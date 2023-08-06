from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Family


class BindFamilyAccounts:

    def __init__(self, main_acc, child_acc):
        self._child_account = child_acc.get('id')
        self._child_role = 'child'
        self._main_account = main_acc.get('id')

    def with_child_role(self):
        self._child_role = 'child'
        return self

    def with_spouse_role(self):
        self._child_role = 'spouse'
        return self

    def generate(self):
        family = Family(child_account=self._child_account,
                        child_role=self._child_role,
                        main_account=self._main_account)

        family.save()
        return model_to_dict(family)
