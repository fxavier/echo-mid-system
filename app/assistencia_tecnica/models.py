from django.db import models
from django.conf import settings

TIPO_PROBLEMA = (
    ('Antigo', 'Antigo'),
    ('Novo', 'Novo')
)

STATUS = (
    ('Pendente', 'Pendente'),
    ('Resolvido', 'Resolvido')
)


class Provincia(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Distrito(models.Model):
    nome = models.CharField(max_length=255)
    provincia = models.ForeignKey(
        Provincia, related_name='distritos',  on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class UnidadeSanitaria(models.Model):
    nome = models.CharField(max_length=255)
    distrito = models.ForeignKey(
        Distrito, related_name='unidades_sanitarias', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Sector(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Area(models.Model):
    nome = models.CharField(max_length=255)
    sector = models.ForeignKey(
        Sector, related_name='areas', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Indicador(models.Model):
    nome = models.CharField(max_length=500)
    area = models.ForeignKey(
        Area, related_name='indicadores', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class FichaAssistenciaTecnica(models.Model):
    nome_responsavel = models.CharField(max_length=255)
    nome_provedor = models.CharField(max_length=255)
    problemas_identificados = models.TextField()
    tipo_problema = models.CharField(max_length=100, choices=TIPO_PROBLEMA)
    atcividades_realizar_resolver_problema = models.CharField(max_length=255)
    nome_pessoa_responsavel_resolver = models.CharField(max_length=255)
    email_pessoa_responsavel_resolver = models.CharField(max_length=255)
    prazo = models.DateField()
    nome_beneficiario_at = models.CharField(max_length=255)
    unidades_sanitaria = models.ForeignKey(
        UnidadeSanitaria, related_name="fichas", on_delete=models.CASCADE)
    indicador = models.ForeignKey(
        Indicador, related_name="fichas", on_delete=models.CASCADE)
    comentarios = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=STATUS, default="Pendente")
    feito_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='fichas',
        on_delete=models.CASCADE
    )
    feito_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.indicador.nome
