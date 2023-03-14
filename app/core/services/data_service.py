import requests
from django.db.models import Q
from dataclasses import dataclass
from core.models import Visit, MissedAppointment, PatientEligibleVLCollection, ViralLoadTestResult, GlobalProperty, DatabaseConfig
from core.utils.date_conversion import DateConversion
from core.utils.database_config import get_database_config
from datetime import datetime, timedelta, date


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
                missed_appointment, created = MissedAppointment.objects.get_or_create(
                    province=database_conf.province,
                    district=data['Distrito'],
                    health_facility=data['us'],
                    patient_id=data['patient_id'],
                    patient_name=data['nome'],
                    patient_identifier=data['NID'],
                    age=data['idade_actual'],
                    phone_number=data['Telefone'],
                    last_appointment_date=DateConversion().convert_str_date(
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
                vl_eligibility, created = PatientEligibleVLCollection.objects.get_or_create(
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
                vl_test_result, created = ViralLoadTestResult.objects.get_or_create(
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
    def post_sms_reminder(cls):
        payload_list = []
        visit = Visit.objects.exclude(phone_number=None).filter(synced=False)
        for v in visit:
            phone = v.phone_number.strip()
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "phone": phone[:9],
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": "463089",
                "active": "1",
            }

            data_values = {
                "patient_identifier": v.patient_identifier,
                "appointment_date": '{:%Y-%m-%d}'.format(v.next_appointment_date),
                "gender": v.gender,
                "pregnant": v.pregnant,
                "age": v.age,
                "district": v.district,
                "province": v.province,
                "health_facility": v.health_facility
            }

            payload['property'] = data_values
            payload_list.append(payload)

            v.synced = True
            v.save()

        records = 0
        records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                    records_not_sent.append(data.copy())
            print(f'Recordes not sent: {records_not_sent}')

        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def post_missed_appointment(cls):
        payload_list = []
        missed_appointment = MissedAppointment.objects.exclude(
            phone_number=None)
        for m in missed_appointment:
            phone = m.phone_number.strip()
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "phone": phone[:9],
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": "485273",
                "active": "1",
            }

            data_values = {
                "patient_identifier": m.patient_identifier,
                "last_appointment_date": '{:%Y-%m-%d}'.format(m.last_appointment_date),
                "gender": m.gender,
                "pregnant": m.pregnant,
                "age": m.age,
                "district": m.district,
                "province": m.province,
                "health_facility": m.health_facility
            }

            payload['property'] = data_values
            payload_list.append(payload)

            m.synced = True
            m.save()

        records = 0
        records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                    records_not_sent.append(data.copy())

            print(f'Records not sent: {records_not_sent}')

        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def post_eligible_for_vl(cls):
        payload_list = []
        vl_eligibility = PatientEligibleVLCollection.objects.exclude(phone_number=None).filter(
            synced=False)
        for e in vl_eligibility:
            phone = e.phone_number.strip()
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "phone": phone[:9],
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": "696884",
                "active": "1",
            }

            data_values = {
                "patient_identifier": e.patient_identifier,
                "gender": "",
                "pregnant": e.pregnant,
                "age": e.age,
                "district": e.district,
                "province": e.province,
                "health_facility": e.health_facility
            }

            payload['property'] = data_values
            payload_list.append(payload)

            e.synced = True
            e.save()

        records = 0
        records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                    records_not_sent.append(data.copy())

            print(f'Records not sent: {records_not_sent}')

        except requests.exceptions.RequestException as err:
            print(err)

    @classmethod
    def post_vl_test_result(cls):
        payload_list = []
        vl_test_result = ViralLoadTestResult.objects.exclude(phone_number=None).filter(
            synced=False)
        for t in vl_test_result:
            phone = t.phone_number.strip()
            payload = {
                "api_key": cls.database_conf.viamo_api_public_key,
                "phone": phone[:9],
                "receive_voice": "1",
                "receive_sms": "1",
                "preferred_channel": "1",
                "groups": "696885",
                "active": "1",
            }

            data_values = {
                "patient_identifier": t.patient_identifier,
                "gender": "",
                "pregnant": t.pregnant,
                "age": t.age,
                "district": t.district,
                "province": t.province,
                "health_facility": t.health_facility
            }

            payload['property'] = data_values
            payload_list.append(payload)

            t.synced = True
            t.save()

        records = 0
        records_not_sent = []
        try:
            for data in payload_list:
                response = requests.post(
                    cls.database_conf.viamo_api_url, json=data)
                print(f'Sending {records} of {len(payload_list)} Records')
                if response.status_code == 200:
                    records += 1
                else:
                    records_not_sent.append(data.copy())

            print(f'Records not sent: {records_not_sent}')

        except requests.exceptions.RequestException as err:
            print(err)
