from django.db import models
from gestao.models import Estabelecimento, Paciente

# Create your models here.
class Campanha(models.Model):
    titulo = models.CharField(max_length=255)
    data_inicio = models.DateField(u'Data de inicio', null=True)
    data_fim = models.DateField(u'Data de fim', null=True)
    estabelecimentos = models.ManyToManyField(Estabelecimento)

    def __str__(self):
        return self.titulo

class Agendamento(models.Model):
    OCUPADO = 'Ocupado'
    DISPONIVEL = 'Disponível'
    APLICADA = 'Aplicada'
    STATUS_CHOICE = (
        (OCUPADO, OCUPADO),
        (APLICADA, APLICADA),
        (DISPONIVEL, DISPONIVEL),
    )
    status = models.CharField('Status', max_length=30, choices=STATUS_CHOICE, default=DISPONIVEL)
    data = models.DateField(u'Data de Vacinação')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)


class Estoque(models.Model):
    quantidade = models.IntegerField('Quantidade de Vacinas')
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)



