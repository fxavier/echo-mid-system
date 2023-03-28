import graphene
from graphene_django.types import DjangoObjectType
from assistencia_tecnica.models import Provincia, Distrito, UnidadeSanitaria, Sector, Area, Indicador, FichaAssistenciaTecnica
from graphql import GraphQLError
from django.db.models import Q
from users.schema import UserType


class ATProvinciaType(DjangoObjectType):
    class Meta:
        model = Provincia


class DistritoType(DjangoObjectType):
    class Meta:
        model = Distrito


class UnidadeSanitariaType(DjangoObjectType):
    class Meta:
        model = UnidadeSanitaria


class ATSectorType(DjangoObjectType):
    class Meta:
        model = Sector


class AreaType(DjangoObjectType):
    class Meta:
        model = Area


class IndicadorType(DjangoObjectType):
    class Meta:
        model = Indicador


class FichaAssistenciaTecnicaType(DjangoObjectType):
    class Meta:
        model = FichaAssistenciaTecnica


class Query:
    at_provincia = graphene.List(ATProvinciaType)
   # provincia = graphene.Field(ProvinciaType, id=graphene.Int(required=True))
    distritos = graphene.List(DistritoType)
    distritos_by_province = graphene.List(
        DistritoType, provincia_id=graphene.Int(required=True))
    unidades_sanitarias = graphene.List(UnidadeSanitariaType)
    unidades_sanitarias_by_district = graphene.List(
        UnidadeSanitariaType, distrito_id=graphene.Int(required=True))
    # at_sectores =
    all_sectores = graphene.List(ATSectorType)
    sector = graphene.List(ATSectorType, id=graphene.Int(required=True))
    areas = graphene.List(AreaType)
    area_by_sector = graphene.List(
        AreaType, sector_id=graphene.Int(required=True))
    indicadores = graphene.List(IndicadorType)
    indicador_by_area = graphene.List(
        IndicadorType, area_id=graphene.Int(required=True))
    fichas = graphene.List(FichaAssistenciaTecnicaType)

    def resolve_at_provincia(self, info):
        return Provincia.objects.all().order_by('-id')

    def resolve_distritos(self, info, search=None):
        if search:
            filter = (
                Q(provincia__nome__icontains=search) |
                Q(nome__icontains=search)
            )
            return Distrito.objects.filter(filter).order_by('-id')
        return Distrito.objects.all().order_by('-id')

    def resolve_distritos_by_province(self, info, provincia_id):
        provincia = Provincia.objects.get(id=provincia_id)
        return Distrito.objects.filter(provincia=provincia).order_by('-id')

    def resolve_unidades_sanitarias(self, info, search=None):
        if search:
            filter = (
                Q(provincia__nome__icontains=search) |
                Q(distrito__nome__icontains=search) |
                Q(nome__icontains=search)
            )
            return UnidadeSanitaria.objects.filter(filter).order_by('-id')
        return UnidadeSanitaria.objects.all().order_by('-id')

    def resolve_unidades_sanitarias_by_district(self, info, distrito_id):
        distrito = Distrito.objects.get(id=distrito_id)
        return UnidadeSanitaria.objects.filter(distrito=distrito)

    # def resolve_at_sectores(self, info, search=None):
    #     if search:
    #         filter = (
    #             Q(nome__icontains=search)
    #         )
    #         return Sector.objects.filter(filter).order_by('-id')
    #     return Sector.objects.all().order_by('-id')

    def resolve_all_sectores(self, info):
        return Sector.objects.all()

    def resolve_areas(self, info):
        # if search:
        #     filter = (
        #         Q(sector__nome__icontains=search) |
        #         Q(nome__icontains=search)
        #     )
        #     return Area.objects.filter(filter).order_by('-id')
        return Area.objects.all().order_by('-id')

    def resolve_area_by_sector(self, info, sector_id):
        sector = Sector.objects.get(id=sector_id)
        return Area.objects.filter(sector=sector).order_by('-id')

    def resolve_indicadores(self, info):
        # if search:
        #     filter = (
        #         Q(area__nome__icontains=search) |
        #         Q(nome__icontains=search)
        #     )
        #     return Indicador.objects.filter(filter).order_by('-id')
        return Indicador.objects.all().order_by('-id')

    def resolve_indicador_by_area(self, info, area_id):
        area = Area.objects.get(id=area_id)
        return Indicador.objects.filter(area=area).order_by('-id')

    def resolve_fichas(self, info):
        # if search:
        #     filter = (
        #         Q(nome_responsavel__icontains=search) |
        #         Q(nome_provedor__icontains=search) |
        #         Q(problemas_identificados__icontains=search) |
        #         Q(tipo_problema__icontains=search) |
        #         Q(nome_pessoa_responsavel_resolver__icontains=search) |
        #         Q(nome_beneficiario_at__icontains=search) |
        #         Q(unidades_sanitaria__nome__icontains=search) |
        #         Q(indicador__nome__icontains=search) |
        #         Q(feito_por__name__icontains=search)
        #     )
        #     return FichaAssistenciaTecnica.objects.filter(filter).order_by('-id')
        return FichaAssistenciaTecnica.objects.all().order_by('-id')


class CreateFicha(graphene.Mutation):
    ficha = graphene.Field(FichaAssistenciaTecnicaType)
    unidade_sanitaria = graphene.Field(UnidadeSanitariaType)
    indicador = graphene.Field(IndicadorType)
    user = graphene.Field(UserType)

    class Arguments:
        nome_responsavel = graphene.String(required=True)
        nome_provedor = graphene.String(required=True)
        problemas_identificados = graphene.String(required=True)
        tipo_problema = graphene.String(required=True)
        atcividades_realizar_resolver_problema = graphene.String(required=True)
        nome_pessoa_responsavel_resolver = graphene.String()
        email_pessoa_responsavel_resolver = graphene.String()
        prazo = graphene.Date()
        nome_beneficiario_at = graphene.String()
        unidades_sanitaria_id = graphene.Int(required=True)
        indicador_id = graphene.Int(required=True)
        comentarios = graphene.String()
        status = graphene.String()
        user_id = graphene.Int(required=True)
        feito_em = graphene.Date()

    def mutate(self, info, **kwargs):
        nome_responsavel = kwargs.get('nome_responsavel')
        nome_provedor = kwargs.get('nome_provedor')
        problemas_identificados = kwargs.get('problemas_identificados')
        tipo_problema = kwargs.get('tipo_problema')
        atcividades_realizar_resolver_problema = kwargs.get(
            'atcividades_realizar_resolver_problema')
        nome_pessoa_responsavel_resolver = kwargs.get(
            'nome_pessoa_responsavel_resolver')
        email_pessoa_responsavel_resolver = kwargs.get(
            'email_pessoa_responsavel_resolver')
        prazo = kwargs.get('prazo')
        nome_beneficiario_at = kwargs.get('nome_beneficiario_at')
        unidade_sanitaria = UnidadeSanitaria.objects.get(
            id=kwargs.get('unidades_sanitaria_id'))
        indicador = Indicador.objects.get(id=kwargs.get('indicador_id'))
        comentarios = kwargs.get('comentarios')
        feito_por = User.objects.get(id=kwargs.get('user_id'))

        ficha = FichaAssistenciaTecnica(
            nome_responsavel=nome_responsavel,
            nome_provedor=nome_provedor,
            problemas_identificados=problemas_identificados,
            tipo_problema=tipo_problema,
            atcividades_realizar_resolver_problema=atcividades_realizar_resolver_problema,
            nome_pessoa_responsavel_resolver=nome_pessoa_responsavel_resolver,
            email_pessoa_responsavel_resolver=email_pessoa_responsavel_resolver,
            prazo=prazo,
            nome_beneficiario_at=nome_beneficiario_at,
            unidades_sanitaria=unidade_sanitaria,
            indicador=indicador,
            comentarios=comentarios,
            feito_por=feito_por

        )
        ficha.save()
        CreateFicha(ficha=ficha)


class Mutation(graphene.ObjectType):
    create_ficha = CreateFicha.Field()
