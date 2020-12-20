from django.db import models
from django.db.models import Sum, Max, Count
from gestao.models import Estabelecimento, Paciente

# Create your models here.
class Campanha(models.Model):
    titulo = models.CharField(max_length=255)
    data_inicio = models.DateField(u'Data de inicio', null=True)
    data_fim = models.DateField(u'Data de fim', null=True)
    estabelecimentos = models.ManyToManyField(Estabelecimento)

    def __str__(self):
        return self.titulo

    def estoque_cadastrado(self):
        if self.estoque_set.exists():
            return self.estoque_set.aggregate(qtd=Sum('quantidade'))['qtd']
    
    def estoque_disponivel(self):
        aplicadas = 0
        if self.estoque_set.exists():
            total_cadastrado = self.estoque_set.aggregate(qtd=Sum('quantidade'))['qtd']
        
        if self.agendamento_set.exists():
            aplicadas = self.agendamento_set.filter(status=Agendamento.APLICADA).aggregate(total=Count('pk'))['total']

        return (total_cadastrado - aplicadas)

    def agendamentos(self):
        if self.agendamento_set.exists():
           return self.agendamento_set.aggregate(total=Count('pk'))['total']
        

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
    lote = models.CharField('Lote', max_length=20, default=None, null=True)


