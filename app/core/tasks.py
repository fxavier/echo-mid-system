from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import DatabaseConfig, MissedAppointment, PatientEligibleVLCollection, ViralLoadTestResult, Visit
from core.services.data_service import AddDataToMiddleware, PostData


@shared_task
def add_arv_dispensing():
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.reminder_uuid)
    AddDataToMiddleware().add_arv_dispensing(instance)


@shared_task
def add_missed_appointments():
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.missed_appointment_uuid)
    AddDataToMiddleware().add_missed_appointments(instance)


@shared_task
def add_eligible_for_vl():
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.viral_load_eligibility_uuid)
    AddDataToMiddleware().add_eligible_for_vl(instance)


@shared_task
def add_vl_test_result():
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.viral_load_test_result_uuid)
    AddDataToMiddleware().add_vl_test_result(instance)


@shared_task
def post_sms_reminder():
    PostData.post_sms_reminder()


@shared_task
def post_missed_appointment():
    PostData.post_missed_appointment()


@shared_task
def post_eligible_for_vl():
    PostData().post_eligible_for_vl()


@shared_task
def post_vl_test_result():
    PostData().post_vl_test_result()


@shared_task
def delete_arv_dispensig():
    Visit.objects.all().delete()


@shared_task
def delete_missed_appointment():
    MissedAppointment.objects.all().delete()


@shared_task
def delete_eligible_for_vl():
    PatientEligibleVLCollection.objects.all().delete()


@shared_task
def delete_vl_test_result():
    ViralLoadTestResult.objects.all().delete()
