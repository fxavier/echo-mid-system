from django.db import models


class Visit(models.Model):
    province = models.CharField(max_length=150)
    district = models.CharField(max_length=150, blank=True, null=True)
    health_facility = models.CharField(max_length=150)
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=255)
    patient_identifier = models.CharField(
        max_length=255, null=True, blank=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    appointment_date = models.DateField()
    next_appointment_date = models.DateField()
    gender = models.CharField(max_length=150)
    community = models.CharField(max_length=500, blank=True, null=True)
    pregnant = models.CharField(max_length=10, default="NAO")
    brestfeeding = models.CharField(max_length=10, default="NAO")
    tb = models.CharField(max_length=10, default="NAO")
    synced = models.BooleanField(default=False)

    def __str__(self):
        return self.patient_name


class MissedAppointment(models.Model):
    province = models.CharField(max_length=150)
    district = models.CharField(max_length=150, blank=True, null=True)
    health_facility = models.CharField(max_length=150, blank=True, null=True)
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=255)
    patient_identifier = models.CharField(
        max_length=255, null=True, blank=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    last_appointment_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=150, blank=True, null=True)
    community = models.CharField(max_length=500, blank=True, null=True)
    pregnant = models.CharField(
        max_length=10, default="NAO", null=True, blank=True)
    drug_pickup_missed_days = models.IntegerField(
        default=0, null=True, blank=True)
    visit_missed_days = models.IntegerField(default=0, null=True, blank=True)
    synced = models.BooleanField(default=False)

    def __str__(self):
        return self.patient_name


class GlobalProperty(models.Model):
    property_name = models.CharField(max_length=100)
    property_value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Global Properties'

    def __str__(self):
        return self.property_name


class DatabaseConfig(models.Model):
    province = models.CharField(max_length=100)
    openmrs_username = models.CharField(max_length=100)
    openmrs_password = models.CharField(max_length=100)
    openmrs_url = models.CharField(max_length=100)
    openmrs_rest_endpoint = models.CharField(max_length=100)
    reminder_uuid = models.CharField(max_length=100)
    missed_appointment_uuid = models.CharField(max_length=100)
    viral_load_eligibility_uuid = models.CharField(max_length=100)
    viral_load_test_result_uuid = models.CharField(max_length=100)
    viamo_api_url = models.CharField(max_length=100)
    viamo_api_public_key = models.CharField(max_length=100)

    def __str__(self):
        return self.province


class PatientEligibleVLCollection(models.Model):
    province = models.CharField(max_length=150)
    district = models.CharField(max_length=150, blank=True, null=True)
    community = models.CharField(max_length=150, blank=True, null=True)
    health_facility = models.CharField(max_length=150, blank=True, null=True)
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=255)
    patient_identifier = models.CharField(
        max_length=255, null=True, blank=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    pregnant = models.CharField(
        max_length=10, default="NAO", null=True, blank=True)
    last_vl_date = models.DateTimeField(null=True, blank=True)
    last_vl_value = models.CharField(max_length=100, null=True, blank=True)
    last_vl_quality = models.CharField(max_length=100, null=True, blank=True)
    synced = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Patient Eligible for VL Collection'
        verbose_name_plural = 'Patients Eligible for VL Collection'

    def __str__(self):
        return self.patient_name


class ViralLoadTestResult(models.Model):
    province = models.CharField(max_length=150)
    district = models.CharField(max_length=150, blank=True, null=True)
    community = models.CharField(max_length=150, blank=True, null=True)
    health_facility = models.CharField(max_length=150, blank=True, null=True)
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=255)
    patient_identifier = models.CharField(
        max_length=255, null=True, blank=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    pregnant = models.CharField(
        max_length=10, default="NAO", null=True, blank=True)
    last_vl_date = models.DateTimeField(null=True, blank=True)
    last_vl_value = models.CharField(max_length=100, null=True, blank=True)
    last_vl_quality = models.CharField(max_length=100, null=True, blank=True)
    synced = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Viral Load Test Result'
        verbose_name_plural = 'Viral Load Test Results'

    def __str__(self):
        return self.patient_name
