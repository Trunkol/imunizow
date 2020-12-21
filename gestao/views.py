from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from gestao.forms import EstabelecimentoForm, PessoaFisicaForm
from agenda.forms import EstoqueForm, AgendamentoForm
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.urls import reverse
from gestao.models import Estabelecimento, Municipio, Estado, \
                            ProfissionalSaude, CoordenadorSus, User
from agenda.models import Campanha, Agendamento

# Create your views here.
@login_required
def estabelecimentos(request):
    if request.user.eh_coordenador_sus():
        estabelecimentos = Estabelecimento.objects.all()
        return render(request, 'gestao/estabelecimentos.html', locals())
    raise PermissionDenied

@login_required
def detalhar_estabelecimento(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    profissionais_saude = ProfissionalSaude.objects.filter(estabelecimento=estabelecimento).only('pessoa_fisica')
    return render(request, 'gestao/detalhar_estabelecimento.html', locals())

@login_required
def editar_estabelecimento(request, pk):
    if request.user.eh_coordenador_sus():
        title = 'Editar Estabelecimento'
        estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
        form = EstabelecimentoForm(request.POST or None, instance=estabelecimento)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(pk,) ))
        return render(request, 'gestao/form_base.html', locals())

    raise PermissionDenied

@login_required
def cadastrar_estabelecimento(request):
    if request.user.eh_coordenador_sus():
        title = 'Cadastrar Estabelecimento'
        form = EstabelecimentoForm(request.POST or None)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(obj.pk,) ))
        return render(request, 'gestao/form_base.html', locals())

    raise PermissionDenied

@login_required
def habilitar_prestador(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    estabelecimento.prestador = True
    estabelecimento.save()
    return HttpResponseRedirect(reverse('gestao:estabelecimentos'))


@transaction.atomic
def adicionar_profissional(request, pk):
    if request.user.eh_coordenador_sus():
        title = 'Adicionar Profissional'
        estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
        form = PessoaFisicaForm(request.POST or None)
        if form.is_valid():
            pessoa_fisica = form.save(commit=False)
            user = User.objects.create_user(form.cleaned_data['cpf'].replace('-', '').replace('.', ''), 
                                            pessoa_fisica.email, 
                                            f'{pessoa_fisica.cpf}{pessoa_fisica.nome}')
            pessoa_fisica.user = user
            pessoa_fisica.save()

            prof_saude = ProfissionalSaude.objects.create(pessoa_fisica=pessoa_fisica, estabelecimento=estabelecimento, ativo=True)

            return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(pk,) ))
        return render(request, 'gestao/form_base.html', locals())

    raise PermissionDenied

@transaction.atomic
def desabilitar_profissional(request, estabelecimento_pk, profissional_pk):
    try:
        prof_saude = ProfissionalSaude.objects.get(id=profissional_pk)
    except ProfissionalSaude.DoesNotExist:
        return HttpResponse(status=404)

    prof_saude.ativo = False
    prof_saude.save()
    
    return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(estabelecimento_pk,) ))


@transaction.atomic
def habilitar_profissional(request, estabelecimento_pk, profissional_pk):
    try:
        prof_saude = ProfissionalSaude.objects.get(id=profissional_pk)
    except ProfissionalSaude.DoesNotExist:
        return HttpResponse(status=404)

    prof_saude.ativo = True
    prof_saude.save()
    
    return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(estabelecimento_pk,) ))


def busca_municipio(request, ibge):
    id = Municipio.objects.filter(codigo=ibge).values('id')[0]
    return JsonResponse(id)

@login_required
def coordenadores_sus(request):
    if request.user.eh_coordenador_sus():
        title = 'Coordenadores SUS'
        coordenadores_sus = CoordenadorSus.objects.all()
        return render(request, 'gestao/coordenadores_sus.html', locals())
    raise PermissionDenied

@login_required
def adicionar_coordenador_sus(request):
    if request.user.eh_coordenador_sus():
        title = 'Adicionar Coordenador SUS'
        form = PessoaFisicaForm(request.POST or None)
        if form.is_valid():
            pessoa_fisica = form.save(commit=False)
            user = User.objects.create_user(form.cleaned_data['cpf'].replace('-', '').replace('.', ''), 
                                            pessoa_fisica.email, 
                                            f'{pessoa_fisica.cpf}{pessoa_fisica.nome}')
            pessoa_fisica.user = user
            pessoa_fisica.save()
            coordenador_sus = CoordenadorSus.objects.create(pessoa_fisica=pessoa_fisica, ativo=True)

            return HttpResponseRedirect(reverse('gestao:coordenadores_sus'))
        return render(request, 'gestao/form_base.html', locals())
    raise PermissionDenied

def desabilitar_coordenador(request, coordenador_pk):
    try:
       coord_sus = CoordenadorSus.objects.get(id=coordenador_pk)
    except CoordenadorSus.DoesNotExist:
        return HttpResponse(status=404)

    coord_sus.ativo = False
    coord_sus.save()
    
    return HttpResponseRedirect(reverse('gestao:coordenadores_sus'))


def habilitar_coordenador(request, coordenador_pk):
    try:
       coord_sus = CoordenadorSus.objects.get(id=coordenador_pk)
    except CoordenadorSus.DoesNotExist:
        return HttpResponse(status=404)

    coord_sus.ativo = True
    coord_sus.save()
    
    return HttpResponseRedirect(reverse('gestao:coordenadores_sus'))

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', locals())

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def gestao_vacinas(request, pk):
    if any((request.user.eh_coordenador_sus(), request.user.eh_profissional_saude())):
        title = 'Gestão de Vacinas'
        estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
        campanhas = estabelecimento.campanha_set.all()
        return render(request, 'gestao/estoque.html', locals())
    raise PermissionDenied


@login_required
def cadastrar_estoque(request, estabelecimento_pk, campanha_pk):
    if any((request.user.eh_coordenador_sus(), request.user.eh_profissional_saude())):
        title = 'Gestão de Vacinas'
        estabelecimento = get_object_or_404(Estabelecimento, pk=estabelecimento_pk)
        campanha = get_object_or_404(Campanha, pk=campanha_pk)
        form = EstoqueForm(request.POST or None, estabelecimento=estabelecimento, campanha=campanha)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gestao:gestao_vacinas', args=(estabelecimento_pk,)))
        return render(request, 'gestao/form_base.html', locals())
    raise PermissionDenied


@login_required
def agendamentos(request, pk):
    title = 'Agendamentos por Campanha'
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    campanhas = estabelecimento.campanha_set.all()
    return render(request, 'gestao/agendamentos.html', locals())

@login_required
def agendamentos_estabelecimento(request, pk):
    title = 'Agendamentos'
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    agendamentos = Agendamento.objects.filter(estabelecimento=estabelecimento, status=Agendamento.OCUPADO).order_by('pk')
    return render(request, 'gestao/agendamentos_estabelecimento.html', locals())


@login_required
def cadastrar_agendamentos(request, estabelecimento_pk, campanha_pk):
    if any((request.user.eh_coordenador_sus(), request.user.eh_profissional_saude())):
        title = 'Cadastrar Agendamento'
        estabelecimento = get_object_or_404(Estabelecimento, pk=estabelecimento_pk)    
        campanha = get_object_or_404(Campanha, pk=campanha_pk)
        form = AgendamentoForm(request.POST or None, estabelecimento=estabelecimento, campanha=campanha)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gestao:agendamentos', args=(estabelecimento_pk,)))
        return render(request, 'gestao/form_base.html', locals())
    raise PermissionDenied