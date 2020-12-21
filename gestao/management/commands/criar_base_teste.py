# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from gestao.models import *
from agenda.models import *
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        camp1, created = Campanha.objects.get_or_create(titulo='Campanha 1', data_inicio=datetime.datetime(2020, 12, 1), data_fim=datetime.datetime(2021, 5, 1))
        camp1.estabelecimentos.add(*range(1, 150))

        camp2, created = Campanha.objects.get_or_create(titulo='Campanha 2', data_inicio=datetime.datetime(2020, 12, 20), data_fim=datetime.datetime(2022, 1, 1))
        camp2.estabelecimentos.add(*range(100, 250))

        prof1 = User.objects.get_or_create(username='prof1', is_staff=True)[0]
        definir_senha(prof1)
        prof1_pf = PessoaFisica.objects.get_or_create(nome='Profissional 1', sexo=u'M', cpf=u'72418687732', data_nascimento='1970-01-01', user=prof1)[0]
        estabprof1 = Estabelecimento.objects.get(pk=20)
        ProfissionalSaude.objects.get_or_create(estabelecimento=estabprof1, pessoa_fisica=prof1_pf, ativo=True)[0]

        prof2 = User.objects.get_or_create(username='prof2', is_staff=True)[0]
        definir_senha(prof2)
        prof2_pf = PessoaFisica.objects.get_or_create(nome='Profissional 1', sexo=u'M', cpf=u'72428687732', data_nascimento='1970-01-01', user=prof2)[0]
        estabprof2 = Estabelecimento.objects.get(pk=50)
        ProfissionalSaude.objects.get_or_create(estabelecimento=estabprof2, pessoa_fisica=prof2_pf, ativo=True)[0]

        coordenador_sus = User.objects.get_or_create(username='coordenador1', is_staff=True)[0]
        definir_senha(coordenador_sus)
        coordenador_sus_pf = PessoaFisica.objects.get_or_create(nome='Coordenador 1', sexo=u'M', cpf=u'97413134039', data_nascimento='1970-01-01', user=coordenador_sus)[0]
        CoordenadorSus.objects.get_or_create(pessoa_fisica=coordenador_sus_pf)[0]
        
        for x in range(50):
            paciente = User.objects.get_or_create(username=f'paciente{x}', is_staff=True)[0]
            definir_senha(paciente)
            paciente_pf = PessoaFisica.objects.get_or_create(nome=f'paciente{x}', sexo=u'M', cpf=f'974131340{x}123', data_nascimento='1970-01-01', user=paciente)[0]
            Paciente.objects.get_or_create(pessoa_fisica=paciente_pf)[0]

        
def definir_senha(usuario):
    usuario.set_password('123')
    usuario.save(0)
