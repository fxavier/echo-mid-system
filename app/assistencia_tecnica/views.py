from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from assistencia_tecnica import serializers
from assistencia_tecnica.models import (Area, Distrito,
                                        FichaAssistenciaTecnica, Indicador,
                                        Provincia, Sector, UnidadeSanitaria)


class apiV1Pagination(PageNumberPagination):
    page_seze = 3


class ProvinciaViewSet(ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = serializers.ProvinciaSerializer


class DistritoViewSet(ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = serializers.DistritoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        provincia_id = self.request.query_params.get('provincia_id', '')
        if provincia_id != '' and provincia_id.isnumeric():
            qs = qs.filter(provincia_id=provincia_id)
        return qs

    def partial_update(self, request, *args, **kwargs):
        distrito = self.get_object()
        serializer = serializers.DistritoSerializer(
            instance=distrito,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )


class UnidadeSanitariaViewSet(ModelViewSet):
    queryset = UnidadeSanitaria.objects.all()
    serializer_class = serializers.UnidadeSanitariaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        distrito_id = self.request.query_params.get('distrito_id', '')
        if distrito_id != '' and distrito_id.isnumeric():
            qs = qs.filter(distrito_id=distrito_id)
        return qs


class SectorViewSet(ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = serializers.SectorSerializer


class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        sector_id = self.request.query_params.get('sector_id', '')
        if sector_id != '' and sector_id.isnumeric():
            qs = qs.filter(sector_id=sector_id)
        return qs


class IndicadorViewSet(ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = serializers.IndicadorSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        area_id = self.request.query_params.get('area_id', '')
        if area_id != '' and area_id.isnumeric():
            qs = qs.filter(area_id=area_id)
        return qs


class FichaViewSet(ModelViewSet):
    queryset = FichaAssistenciaTecnica.objects.all()
    serializer_class = serializers.FichaAssistenciaTecnicaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        unidade_sanitaria_id = self.request.query_params.get(
            'unidade_sanitaria_id', '')
        if unidade_sanitaria_id != '' and unidade_sanitaria_id.isnumeric():
            qs = qs.filter(unidade_sanitaria_id=unidade_sanitaria_id)
        return qs

    def partial_update(self, request, *args, **kwargs):
        ficha = self.get_object()
        serializer = serializers.FichaAssistenciaTecnicaSerializer(
            instance=ficha,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )
