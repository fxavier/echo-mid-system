from __future__ import absolute_import, unicode_literals

from celery import shared_task

from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit)
from core.services.data_service import AddDataToMiddleware, PostData


@shared_task
def pacientes_marcados_para_levantamento_de_arvs():
    Visit.objects.all().delete()
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.reminder_uuid)
    AddDataToMiddleware().add_arv_dispensing(instance)


@shared_task
def pacientes_faltosos_ao_levantamento_ou_consulta():
    MissedAppointment.objects.all().delete()
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.missed_appointment_uuid)
    AddDataToMiddleware().add_missed_appointments(instance)


@shared_task
def pacientes_elegiveis_carga_viral():
    PatientEligibleVLCollection.objects.all().delete()
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.viral_load_eligibility_uuid)
    AddDataToMiddleware().add_eligible_for_vl(instance)


@shared_task
def pacientes_com_carga_viral_alta():
    ViralLoadTestResult.objects.all().delete()
    database_conf = DatabaseConfig.objects.get(pk=1)
    instance = str(database_conf.openmrs_url) \
        + str(database_conf.openmrs_rest_endpoint) \
        + str(database_conf.viral_load_test_result_uuid)
    AddDataToMiddleware().add_vl_test_result(instance)


@shared_task
def Envio_pacientes_marcados_levantamento():
    PostData.post_sms_reminder()


@shared_task
def Envio_faltosos_ao_levantamento_ou_consulta():
    PostData.post_missed_appointment()


@shared_task
def envio_eligiveis_carga_viral():
    PostData().post_eligible_for_vl()


@shared_task
def envio_pacientes_carga_viral_alta():
    PostData().post_vl_test_result()


@shared_task
def delete_pacientes_marcados_para_levantamento():
    Visit.objects.all().delete()


@shared_task
def delete_faltosos_levantemento_ou_consulta():
    MissedAppointment.objects.all().delete()


@shared_task
def delete_elegiveis_carga_viral():
    PatientEligibleVLCollection.objects.all().delete()


@shared_task
def delete_pacientes_com_carga_viral_alta():
    ViralLoadTestResult.objects.all().delete()
