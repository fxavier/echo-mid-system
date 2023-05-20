from rest_framework import serializers
from users.models import User

from assistencia_tecnica.models import (Area, Distrito,
                                        FichaAssistenciaTecnica, Indicador,
                                        Provincia, Sector, UnidadeSanitaria)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        read_only_fields = ('id',)


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provincia
        fields = ['id', 'nome']
        read_only_fields = ('id',)


class DistritoSerializer(serializers.ModelSerializer):
    provincia_name = serializers.StringRelatedField(
        source='provincia', read_only=True)

    class Meta:
        model = Distrito
        fields = ['id', 'nome', 'provincia_name', 'provincia']

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UnidadeSanitariaSerializer(serializers.ModelSerializer):
    distrito_name = serializers.StringRelatedField(source='distrito')

    class Meta:
        model = UnidadeSanitaria
        fields = ['id', 'nome', 'distrito', 'distrito_name']
        read_only_fields = ('id', 'distrito_name')


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'nome']
        read_only_fields = ('id',)


class AreaSerializer(serializers.ModelSerializer):
    sector_name = serializers.StringRelatedField(source='sector')

    class Meta:
        model = Area
        fields = ['id', 'nome', 'sector', 'sector_name']
        read_only_fields = ('id', 'sector_name')


class IndicadorSerializer(serializers.ModelSerializer):
    area_name = serializers.StringRelatedField(source='area')

    class Meta:
        model = Indicador
        fields = ['id', 'nome', 'area', 'area_name']
        read_only_fields = ('id', 'area_name')


class FichaAssistenciaTecnicaSerializer(serializers.ModelSerializer):
    indicador_name = serializers.StringRelatedField(source='indicador')
    autor = serializers.StringRelatedField(source='feito_por')
    unidades_sanitaria_name = serializers.StringRelatedField(
        source='unidades_sanitaria')

    class Meta:
        model = FichaAssistenciaTecnica
        fields = ['id', 'unidades_sanitaria', 'unidades_sanitaria_name',
                  'indicador',
                  'indicador_name', 'nome_responsavel', 'nome_provedor',
                  'problemas_identificados', 'tipo_problema',
                  'atcividades_realizar_resolver_problema',
                  'nome_pessoa_responsavel_resolver',
                  'email_pessoa_responsavel_resolver',
                  'prazo', 'nome_beneficiario_at',
                  'feito_por', 'autor', 'feito_em', 'comentarios',
                  ]
        read_only_fields = ('id', 'unidades_sanitaria_name',
                            'indicador_name', 'autor',)
