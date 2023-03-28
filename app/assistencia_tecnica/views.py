from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from assistencia_tecnica.models import Provincia, Distrito, UnidadeSanitaria, Sector, Area, Indicador, FichaAssistenciaTecnica

from assistencia_tecnica import serializers


def _params_to_int(qs):
        return int(qs)

class ProvinciaViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Provincia.objects.all()
    serializer_class = serializers.ProvinciaSerializer
    

    
class DistritoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Distrito.objects.all()
    serializer_class = serializers.DistritoSerializer
   
    
    def get_queryset(self):

        provincia = self.request.query_params.get('provincia')
        queryset = self.queryset
        
        if provincia:
            provincia_id = _params_to_int(provincia)
            queryset = queryset.filter(provincia__id=provincia_id)
        return queryset
    
class UnidadeSanitariaViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = UnidadeSanitaria.objects.all()
    serializer_class = serializers.UnidadeSanitariaSerializer
    
    
    def get_queryset(self):
        
        distrito = self.request.query_params.get('distrito')
        queryset = self.queryset
        
        if distrito:
            distrito_id = _params_to_int(distrito)
            queryset = queryset.filter(distrito__id=distrito_id)
        
        return queryset
    
    
class SectorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Sector.objects.all()
    serializer_class = serializers.SectorSerializer
   
   
    
class AreaViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerializer
   
   
    
    def get_queryset(self):
        
        sector = self.request.query_params.get('sector')
        queryset = self.queryset
        
        if sector:
            sector_id = _params_to_int(sector)
            queryset = queryset.filter(sector__id=sector_id)
        return queryset
    
    
class IndicadorViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Indicador.objects.all()
    serializer_class = serializers.IndicadorSerializer
    
    
    
    def get_queryset(self):
        
        area = self.request.query_params.get('area')
        queryset = self.queryset
        
        if area:
            area_id = _params_to_int(area)
            queryset = queryset.filter(area__id=area_id)
        
        return queryset
    
    
class FichaAssistenciaTecnicaViewSet(viewsets.GenericViewSet,
                                     mixins.ListModelMixin,
                                     mixins.CreateModelMixin):
    queryset = FichaAssistenciaTecnica.objects.all()
    serializer_class = serializers.FichaAssistenciaTecnicaSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    
    # def _params_to_ints(self, qs):
    #     return [int(str_id) for str_id in qs.split(',')]
    
    def get_queryset(self):
        indicador = self.request.query_params.get('indicador')
        unidade_sanitaria = self.request.query_params.get('unidade_sanitaria')
        
        queryset = self.queryset
        
        if indicador:
            indicador_id = _params_to_int(indicador)
            queryset = queryset.filter(indicador__id=indicador_id)
        if unidade_sanitaria:
            us_id = _params_to_int(unidade_sanitaria)
            queryset = queryset.filter(unidade_sanitaria__id=us_id)
        return queryset #.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.FichaAssistenciaTecnicaDetailSerializer
       
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()
        
