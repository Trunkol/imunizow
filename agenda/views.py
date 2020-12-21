from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from gestao.forms import PessoaFisicaForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from gestao.models import Paciente, PessoaFisica, User, Estabelecimento
from django.db import transaction
from agenda.forms import CampanhaForm, AgendarVacinacaoEstabelecimentoForm, \
                         AgendarVacinacaoDataForm, ConfirmacaoVacinaForm, \
                         VacinaPrivadaForm
from agenda.models import Campanha, Agendamento, Vacina, VacinaPrivada
from datetime import datetime, date
from django.core.mail import send_mail
        
@login_required
def index(request):    
    minhas_vacinas = Agendamento.objects.filter(paciente=request.user.paciente(), 
                                        status__in=[Agendamento.APLICADA, Agendamento.OCUPADO])
    vacinas_pendentes = Agendamento.objects.filter(paciente=request.user.paciente())
    campanhas_ativas = Campanha.objects.filter(data_inicio__lte=date.today(), 
                                                        data_fim__gte=date.today())
    campanhas_sem_agendas = campanhas_ativas.exclude(pk__in=minhas_vacinas.values_list('campanha', flat=True))
    
    return render(request, 'agenda/index.html', locals())

@login_required
@transaction.atomic
def autocadastro(request):
    title = 'Autocadastro de Paciente'
    instance = PessoaFisica.objects.filter(cpf=request.user.username).first()
    form = PessoaFisicaForm(data=request.POST or None, instance=instance)
    if form.is_valid():
        pessoa_fisica = form.save(commit=False)
        user, created = User.objects.get_or_create(username=form.cleaned_data['cpf'].replace('-', '').replace('.', ''))
        pessoa_fisica.user = user
        pessoa_fisica.save()

        paciente = Paciente.objects.create(pessoa_fisica=pessoa_fisica)

        return HttpResponseRedirect(reverse('agenda:index'))
    return render(request, 'gestao/form_base.html', locals())


@login_required
def minhas_vacinas(request, paciente_pk):
    title = 'Minhas Vacinas'
    paciente = get_object_or_404(Paciente, pk=paciente_pk)    
    vacinas_publicas = Vacina.objects.filter(paciente=paciente)
    vacinas_privadas = VacinaPrivada.objects.filter(paciente=paciente)

    return render(request, 'agenda/minhas_vacinas.html', locals())


@login_required
def campanhas(request):
    title = 'Campanhas'
    campanhas = Campanha.objects.all()
    return render(request, 'agenda/campanhas.html', locals())


@login_required
def detalhar_campanha(request, pk):
    title = 'Campanhas'
    return render(request, 'agenda/minhas_vacinas.html', locals())


@login_required
def editar_campanha(request, pk):
    title = 'Editar Campanha'
    campanha = get_object_or_404(Campanha, pk=pk)    
    form = CampanhaForm(data=request.POST or None, instance=campanha)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('agenda:campanhas'))
    return render(request, 'gestao/form_base.html', locals())


@login_required
def cadastrar_campanha(request):
    title = 'Campanhas'
    form = CampanhaForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('agenda:campanhas'))
    return render(request, 'gestao/form_base.html', locals())

@login_required
def cadastrar_campanha(request):
    title = 'Campanhas'
    form = CampanhaForm(data=request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('agenda:campanhas'))
    return render(request, 'gestao/form_base.html', locals())

@login_required
def agendar_vacinacao_estabelecimento(request, campanha_pk):
    title = 'Agendar Vacinação - Escolha de Estabelecimento'
    campanha = get_object_or_404(Campanha, pk=campanha_pk)
    form = AgendarVacinacaoEstabelecimentoForm(data=request.POST or None, campanha=campanha)
    if form.is_valid():
        estabelecimento = form.cleaned_data['estabelecimento']
        return HttpResponseRedirect(reverse('agenda:agendar_vacinacao_data', args=(campanha.pk, estabelecimento.pk)))
    return render(request, 'gestao/form_base.html', locals())

@login_required
def agendar_vacinacao_data(request, campanha_pk, estabelecimento_pk):
    title = 'Agendar Vacinação - Escolha da Data'
    campanha = get_object_or_404(Campanha, pk=campanha_pk)
    estabelecimento = get_object_or_404(Estabelecimento, pk=estabelecimento_pk)
    paciente = request.user.paciente()
    form = AgendarVacinacaoDataForm(data=request.POST or None, campanha=campanha,
                                     estabelecimento=estabelecimento, paciente=paciente)
    if form.is_valid():
        form.save()
        #send_mail('[IMUNIZOW] Vacina Agendada', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=True)
        return HttpResponseRedirect(reverse('agenda:index'))
    return render(request, 'gestao/form_base.html', locals())

@login_required
def fila(request, agendamento_pk):
    title = 'Fila de Vacinação'
    agendamento = get_object_or_404(Agendamento, pk=agendamento_pk)
    campanha = get_object_or_404(Campanha, pk=agendamento.campanha.pk)
    estabelecimento = get_object_or_404(Estabelecimento, pk=agendamento.estabelecimento.pk)
    agendamentos = Agendamento.objects.filter(campanha=campanha, estabelecimento=estabelecimento, 
                                                    data=agendamento.data, status=Agendamento.OCUPADO).order_by('pk')
    return render(request, 'agenda/fila.html', locals())

@login_required
def confirmar_vacinacao(request, agendamento_pk):
    title = 'Confirmar Vacinação'
    agendamento = get_object_or_404(Agendamento, pk=agendamento_pk)
    form = ConfirmacaoVacinaForm(data=request.POST or None, agendamento=agendamento)
    if form.is_valid():
        form.save()
        #ProfissionalSaude.objects.filter(estabelecimento=agendamento.estabelecimento)
        #send_mail('[IMUNIZOW] Vacina Aplicada', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=True)
        return HttpResponseRedirect(reverse('gestao:agendamentos_estabelecimento', args=(agendamento.estabelecimento.pk,)))
    return render(request, 'gestao/form_base.html', locals())

@login_required
def cadastrar_vacina_privada(request):
    title = 'Cadastro de Vacina Privada'
    paciente = request.user.paciente()
    form = VacinaPrivadaForm(data=request.POST or None, paciente=paciente)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('agenda:index'))
    return render(request, 'gestao/form_base.html', locals())
