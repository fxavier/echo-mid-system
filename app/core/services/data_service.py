from dataclasses import dataclass
from datetime import date, timedelta

import requests
from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit)
from core.utils.date_conversion import DateConversion


@dataclass
class FetchOpenMRSData:

    def get_arv_dispensing(self, instance):
        database_conf = DatabaseConfig.objects.get(pk=1)
        auth = (str(database_conf.openmrs_username),
                str(database_conf.openmrs_password))
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=5)
        params = {
            'startDate': str(start_date),
            'endDate': str(end_date)
        }
        try:
            response = requests.get(
                instance, params=params, auth=auth)
            data_list = response.json()['rows']
            return data_list
        except requests.exceptions.RequestException as err:
            print(err)

    def get_misssed_appointment(self, instance):
        database_conf = DatabaseConfig.objects.get(pk=1)
        auth = (str(database_conf.openmrs_username),
                str(database_conf.openmrs_password))
        end_date = date.today() - timedelta(days=2)
        params = {
            'endDate': str(end_date)
        }
        try:
            response = requests.get(
                instance, params=params, auth=auth)

            data_list = response.json()['rows']
            return data_list
        except requests.exceptions.RequestException as err:
            print(err)

    def get_eligible_for_vl(self, instance):
        database_conf = DatabaseConfig.objects.get(pk=1)
        auth = (str(database_conf.openmrs_username),
                str(database_conf.openmrs_password))
        end_date = date.today()
        params = {
            'endDate': str(end_date)
        }
        try:
            response = requests.get(
                instance, params=params, auth=auth)
            data_list = response.json()['rows']
            return data_list
        except requests.exceptions.RequestException as err:
            print(err)

    def get_vl_test_result(self, instance):
        database_conf = DatabaseConfig.objects.get(pk=1)
        auth = (str(database_conf.openmrs_username),
                str(database_conf.openmrs_password))
        end_date = date.today()
        params = {
            'endDate': str(end_date)
        }
        try:
            response = requests.get(
                instance, params=params, auth=auth)
            data_list = response.json()['rows']
            return data_list
        except requests.exceptions.RequestException as err:
            print(err)


@dataclass
class AddDataToMiddleware:
    @staticmethod
    def add_arv_dispensing(instance):
        database_conf = DatabaseConfig.objects.get(pk=1)

        data_list = FetchOpenMRSData().get_arv_dispensing(instance)

        if data_list is not None:
            for data in data_list:
                visit, created = Visit.objects.get_or_create(
                    province=database_conf.province,
                    district=data['Distrito'],
                    health_facility=data['us'],
                    patient_id=data['patient_id'],
                    patient_name=data['NomeCompleto'],
                    patient_identifier=data['NID'],
                    age=data['age'],
                    phone_number=data['phone_number'],
                    appointment_date=DateConversion().convert_str_date(
                        data['dispensing_date']),
                    next_appointment_date=DateConversion().convert_str_date(
                        data['next_dispensing_date']),
                    gender=data['gender'],
                    community=data['Bairro'],
                    pregnant=data['pregnant'],
                    brestfeeding=data['brestfeeding'],
                    tb=data['tb']
                )
                visit.save()

    @staticmethod
    def add_missed_appointments(instance):
        database_conf = DatabaseConfig.objects.get(pk=1)
        data_list = FetchOpenMRSData().get_misssed_appointment(instance)
        if data_list is not None:
            for data in data_list:
                missed_appointment, created = \
                    MissedAppointment.objects.get_or_create(
                        province=database_conf.province,
                        district=data['Distrito'],
                        health_facility=data['us'],
                        patient_id=data['patient_id'],
                        patient_name=data['nome'],
                        patient_identifier=data['NID'],
                        age=data['idade_actual'],
                        phone_number=data['Telefone'],
                        last_appointment_date=DateConversion()
                        .convert_str_date(
                            data['ultimo_lev']),
                        gender=data['gender'],
                        community=data['Bairro'],
                        pregnant=data['p_gestante'],
                        drug_pickup_missed_days=data['dias_falta_lev'],
                        visit_missed_days=data['dias_falta_seg']
                    )

            missed_appointment.save()

    @staticmethod
    def add_eligible_for_vl(instance):
        database_conf = DatabaseConfig.objects.get(pk=1)

        data_list = FetchOpenMRSData().get_eligible_for_vl(instance)

        if data_list is not None:
            for data in data_list:
                vl_eligibility, created = PatientEligibleVLCollection.objects.\
                    get_or_create(
                        province=database_conf.province,
                        district=data['district'],
                        community=data['Bairro'],
                        health_facility=data['usname'],
                        patient_id=data['patient_id'],
                        patient_name=data['nome'],
                        patient_identifier=data['NID'],
                        age=data['idade_actual'],
                        phone_number=data['Telefone'],
                        last_vl_date=DateConversion().convert_str_date(
                            data['data_colheita_ucv']),
                        last_vl_value=data['valor_carga'],
                        last_vl_quality=data['qualidade_carga']
                    )
                vl_eligibility.save()

    @staticmethod
    def add_vl_test_result(instance):
        database_conf = DatabaseConfig.objects.get(pk=1)

        data_list = FetchOpenMRSData().get_vl_test_result(instance)

        if data_list is not None:
            for data in data_list:
                vl_test_result, created = ViralLoadTestResult.objects\
                    .get_or_create(
                        province=database_conf.province,
                        district=data['district'],
                        community=data['Bairro'],
                        health_facility=data['usname'],
                        patient_id=data['patient_id'],
                        patient_name=data['NomeCompleto'],
                        patient_identifier=data['NID'],
                        age=data['idade_actual'],
                        phone_number=data['contacto'],
                        pregnant=data['gravida'],
                        last_vl_date=DateConversion().convert_str_date(
                            data['data_cv']),
                        last_vl_value=data['cv']
                    )
                vl_test_result.save()


@dataclass
class PostData:
    database_conf = DatabaseConfig.objects.get(pk=1)

    @classmethod
    def create_payload(cls, queryset, group_id, date_attribute=None):
        payload_list = []
        for item in queryset:
            phone = item.phone_number.strip()
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "phone": phone[:9],
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": group_id,
                "active": "1",
            }

            data_values = {
                "patient_identifier": item.patient_identifier,
                "gender": item.gender,
                "pregnant": item.pregnant,
                "age": item.age,
                "district": item.district,
                "province": item.province,
                "health_facility": item.health_facility
            }
            if date_attribute:
                data_values[date_attribute] = '{:%Y-%m-%d}'.format(
                    getattr(item, date_attribute))

            payload['property'] = data_values
            payload_list.append(payload)

            item.synced = True
            item.save()

        return payload_list

    @classmethod
    def post_data(cls, payload_list):
        records = 0
        records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records + 1} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                    records_not_sent.append(data.copy())
            print(f'Records not sent: {records_not_sent}')
        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def post_sms_reminder(cls):
        queryset = Visit.objects.exclude(
            phone_number=None).filter(synced=False)
        payload_list = cls.create_payload(
            queryset, "463089", "next_appointment_date")
        cls.post_data(payload_list)

    @classmethod
    def post_missed_appointment(cls):
        queryset = MissedAppointment.objects.exclude(phone_number=None)
        payload_list = cls.create_payload(
            queryset, "485273", "last_appointment_date")
        cls.post_data(payload_list)

    @classmethod
    def post_eligible_for_vl(cls):
        queryset = PatientEligibleVLCollection.objects.exclude(
            phone_number=None).filter(synced=False)
        payload_list = cls.create_payload(queryset, "696884")
        cls.post_data(payload_list)

    @classmethod
    def post_vl_test_result(cls):
        queryset = ViralLoadTestResult.objects.exclude(
            phone_number=None).filter(synced=False)
        payload_list = cls.create_payload(queryset, "696885")
        cls.post_data(payload_list)
