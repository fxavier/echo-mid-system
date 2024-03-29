from assistencia_tecnica.models import (Area, Distrito,
                                        FichaAssistenciaTecnica, Indicador,
                                        Provincia, Sector, UnidadeSanitaria)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from import_export.admin import ImportExportMixin
from users.models import User

from core.models import (DatabaseConfig, MissedAppointment,
                         PatientEligibleVLCollection, ViralLoadTestResult,
                         Visit)


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class VisitAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'id', 'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'gender', 'appointment_date', 'next_appointment_date', 'synced'
    ]


class MissedAppointmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'id', 'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'gender', 'last_appointment_date', 'synced'
    ]


class PatientEligibleVLCollectionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'id', 'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'last_vl_date', 'last_vl_value', 'last_vl_quality', 'synced'
    ]


class ViralLoadTestResultAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'id', 'province', 'district', 'health_facility', 'patient_identifier',
        'age', 'last_vl_date', 'last_vl_value', 'last_vl_quality', 'synced'
    ]


class GlobalPropertyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['property_name', 'property_value']


class DatabaseConfigAdmin(ImportExportMixin, admin.ModelAdmin):

    list_display = [
        'province', 'openmrs_username', 'openmrs_password', 'openmrs_url',
        'openmrs_rest_endpoint', 'reminder_uuid', 'missed_appointment_uuid',
        'viral_load_eligibility_uuid', 'viral_load_test_result_uuid',
        'viamo_api_url', 'viamo_api_public_key'
    ]


class ProvinciaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']


class DistritoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'provincia']


class UnidadeSanitariaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'distrito']


class SectorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']


class AreaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'sector']


class IndicadorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'area']


class FichaAssistenciaTecnicaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome_responsavel', 'nome_provedor',
                    'problemas_identificados', 'tipo_problema',
                    'atcividades_realizar_resolver_problema'
                    ]


admin.site.register(User, UserAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(MissedAppointment, MissedAppointmentAdmin)
admin.site.register(PatientEligibleVLCollection,
                    PatientEligibleVLCollectionAdmin)
admin.site.register(ViralLoadTestResult, ViralLoadTestResultAdmin)
# admin.site.register(GlobalProperty, GlobalPropertyAdmin)
admin.site.register(DatabaseConfig, DatabaseConfigAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Distrito, DistritoAdmin)
admin.site.register(UnidadeSanitaria, UnidadeSanitariaAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Indicador, IndicadorAdmin)
admin.site.register(FichaAssistenciaTecnica, FichaAssistenciaTecnicaAdmin)

admin.site.site_header = 'ECHO MID SYSTEM'
