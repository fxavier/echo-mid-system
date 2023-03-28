from rest_framework import serializers


from assistencia_tecnica.models import Provincia, Distrito, UnidadeSanitaria, Sector, Area, Indicador, FichaAssistenciaTecnica
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        read_only_fields = ('id',)


class ProvinciaSerializer(serializers.ModelSerializer):
    #distritos = serializers.StringRelatedField(many=True)

    class Meta:
        model = Provincia
        fields = ['id', 'nome']
        read_only_fields = ('id',)


class DistritoSerializer(serializers.ModelSerializer):
    provincia = ProvinciaSerializer()
   # provincia = serializers.StringRelatedField(many=False)
   # unidades_sanitarias = serializers.StringRelatedField(many=True)

    class Meta:
        model = Distrito
        fields = ['id', 'nome', 'provincia']
        read_only_fields = ('id',)


class UnidadeSanitariaSerializer(serializers.ModelSerializer):
    distrito = DistritoSerializer()

    class Meta:
        model = UnidadeSanitaria
        fields = ['id', 'nome', 'distrito']
        read_only_fields = ('id',)


class SectorSerializer(serializers.ModelSerializer):
   # areas = serializers.StringRelatedField(many=True)

    class Meta:
        model = Sector
        fields = ['id', 'nome']
        read_only_fields = ('id',)


class AreaSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
   # indicadores = serializers.StringRelatedField(many=True)

    class Meta:
        model = Area
        fields = ['id', 'nome', 'sector']
        read_only_fields = ('id',)


class IndicadorSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Indicador
        fields = ['id', 'nome', 'area']
        read_only_fields = ('id',)


class FichaAssistenciaTecnicaSerializer(serializers.ModelSerializer):
    # indicador = serializers.PrimaryKeyRelatedField(
    #     queryset=Indicador.objects.all())
    # feito_por = serializers.StringRelatedField()
    # unidades_sanitaria = serializers.PrimaryKeyRelatedField(
    #     queryset=UnidadeSanitaria.objects.all())
    unidades_sanitaria = UnidadeSanitariaSerializer()
    indicador = IndicadorSerializer()
    feito_por = UserSerializer()

    class Meta:
        model = FichaAssistenciaTecnica
        fields = ['id', 'unidades_sanitaria', 'indicador', 'nome_responsavel', 'nome_provedor',
                  'problemas_identificados', 'tipo_problema', 'atcividades_realizar_resolver_problema',
                  'nome_pessoa_responsavel_resolver', 'email_pessoa_responsavel_resolver', 'prazo', 'nome_beneficiario_at',
                  'feito_por', 'feito_em', 'comentarios'
                  ]
        read_only_fields = ('id',)


class FichaAssistenciaTecnicaDetailSerializer(FichaAssistenciaTecnicaSerializer):
    indicador = IndicadorSerializer
    unidades_sanitaria = UnidadeSanitariaSerializer
