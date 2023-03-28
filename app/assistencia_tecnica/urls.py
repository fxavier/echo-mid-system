from django.urls import path, include
from rest_framework.routers import DefaultRouter

from assistencia_tecnica import views

router = DefaultRouter()
router.register('provincias', views.ProvinciaViewSet)
router.register('distritos', views.DistritoViewSet)
router.register('unidades-sanitarias', views.UnidadeSanitariaViewSet)
router.register('sectores', views.SectorViewSet)
router.register('areas', views.AreaViewSet)
router.register('indicadores', views.IndicadorViewset)
router.register('fichas', views.FichaAssistenciaTecnicaViewSet)

app_name = 'assistencia_tecnica'

urlpatterns = [
    path('', include(router.urls)),
]