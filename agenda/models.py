from django.db import models
from gestao.models import Estabelecimento

# Create your models here.
class Campanha(models.Model):
    titulo = models.CharField(max_length=255)
    data_inicio = models.DateField(u'Data de inicio', null=True)
    data_fim = models.DateField(u'Data de fim', null=True)
    estabelecimentos = models.ManyToManyField(Estabelecimento)