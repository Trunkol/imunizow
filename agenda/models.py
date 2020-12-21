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
        return 0

    def estoque_disponivel(self):
        disponiveis = 0
        if self.estoque_set.exists():
            total_cadastrado = self.estoque_set.aggregate(qtd=Sum('quantidade'))['qtd']
            disponiveis = total_cadastrado

        if self.agendamento_set.exists():
            aplicadas = self.agendamento_set.filter(status=Agendamento.APLICADA).aggregate(total=Count('pk'))['total']
            disponiveis -= aplicadas

        return disponiveis

    def agendamentos(self):
        if self.agendamento_set.exists():
           return self.agendamento_set.aggregate(total=Count('pk'))['total']


class Estoque(models.Model):
    quantidade = models.IntegerField('Quantidade de Vacinas')
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)
    lote = models.CharField('Lote', max_length=20, default=None, null=True)

    def __str__(self):
        return f'{self.campanha.titulo} (Lote: {self.lote})'


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
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, null=True)
    data_aplicacao = models.DateTimeField(u'data_aplicacao', null=True)

    def foi_aplicada(self):
        if self.status == Agendamento.APLICADA:
            return True
        return False

    def foi_marcada(self):
        if self.status == Agendamento.OCUPADO:
            return True
        return False

class Vacina(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, null=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=True)

class VacinaPrivada(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    descricao = models.CharField('Descrição', max_length=255)
    estabelecimento = models.CharField('Estabelecimento de Aplicação', max_length=255)
    data_vacinacao = models.DateField(u'Data de vacinação', null=True)
    lote = models.CharField('Estabelecimento de Aplicação', max_length=255)
    
