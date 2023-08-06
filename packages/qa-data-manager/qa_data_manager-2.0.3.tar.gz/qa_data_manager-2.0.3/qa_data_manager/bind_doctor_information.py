from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import DoctorInformations

"""
Связь доктора с информациией о докторе.
    Поля:
        * user_id - Индентификатор пользовавтелья; Обязательное поле, устанавливается при инциализации класса из параметра user.
        * category - Категория врача; Принимает String значение; По умолчанию Врач высшей категории.
        * description - Оипсание врача; Принимает String значение; По умолчанию.
        * education - Образование врача; Принимает String значение; По умолчанию.
        * experience - Год начала работы врача; Принимает int значение; По умолчанию.
        * license_status - Статус лицензии врача; По умолчанию no_license.
        
    Метод 
        * with_category():
            - Принимает параметр value.
            - Устанавливает в поле category значение value
        * with_description():
            - Принимает параметр value.
            - Устанавливает в поле description значение value
        * with_education():
            - Принимает параметр value.
            - Устанавливает в поле education значение value
        * with_experience():
            - Принимает параметр value.
            - Устанавливает в поле experience значение value
        * with_active_license() - Устанавливает в поле license_status значение active
        * with_citylab_license() - Устанавливает в поле license_status значение citylab
        * with_commission_license() - Устанавливает в поле license_status значение commission
        * with_commission_license_status() - Устанавливает в поле license_status значение commission_license
        * with_inactive_license() - Устанавливает в поле license_status значение inactive
        * with_package_license() - Устанавливает в поле license_status значение package
        * with_showcase_license() - Устанавливает в поле license_status значение showcase
        * generate():
            - Сохраняет объект BindDoctorInformation в базу данных.
            - Возвращает модель таблицы DoctorInformations с данными сгенерированной связи.
"""


class BindDoctorInformation:

    def __init__(self, user):
        self._user_id = user.get('id')
        self._category = 'Врач высшей категории'
        self._description = 'Направление деятельности: Широкий спектр всех возможных в мире заболеваний.'
        self._education = 'ФакМедМос'
        self._experience = 2000
        self._license_status = 'no_license'

    def with_category(self, value):
        self._category = value
        return self

    def with_description(self, value):
        self._description = value
        return self

    def with_education(self, value):
        self._education = value
        return self

    def with_experience(self, value):
        self._experience = value
        return self

    def with_active_license(self):
        self._license_status = 'active'
        return self

    def with_citylab_license(self):
        self._license_status = 'citylab'
        return self

    def with_commission_license(self):
        self._license_status = 'commission'
        return self

    def with_commission_license_status(self):
        self._license_status = 'commission_license'
        return self

    def with_inactive_license(self):
        self._license_status = 'inactive'
        return self

    def with_package_license(self):
        self._license_status = 'package'
        return self

    def with_showcase_license(self):
        self._license_status = 'showcase'
        return self

    def generate(self):
        doctor_information = DoctorInformations(category=self._category,
                                                description=self._description,
                                                education=self._education,
                                                experience=self._experience,
                                                has_pay_before_minutes=0,
                                                license_status=self._license_status,
                                                pay_before_minutes=None,
                                                percent_income_chat=None,
                                                percent_income_online=None,
                                                user=self._user_id)
        doctor_information.save()

        return model_to_dict(doctor_information)
