from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from gestao.forms import EstabelecimentoForm, PessoaFisicaForm
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.urls import reverse
from gestao.models import Estabelecimento, Municipio, Estado, \
                            ProfissionalSaude, CoordenadorSus, User

# Create your views here.
def estabelecimentos(request):
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'gestao/estabelecimentos.html', locals())

def detalhar_estabelecimento(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    profissionais_saude = ProfissionalSaude.objects.filter(estabelecimento=estabelecimento).only('pessoa_fisica')
    return render(request, 'gestao/detalhar_estabelecimento.html', locals())

def editar_estabelecimento(request, pk):
    title = 'Editar Estabelecimento'
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    form = EstabelecimentoForm(request.POST or None, instance=estabelecimento)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(pk,) ))
    return render(request, 'gestao/form_base.html', locals())

def cadastrar_estabelecimento(request):
    title = 'Cadastrar Estabelecimento'
    form = EstabelecimentoForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(obj.pk,) ))
    return render(request, 'gestao/form_base.html', locals())

def habilitar_prestador(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    estabelecimento.prestador = True
    estabelecimento.save()
    return HttpResponseRedirect(reverse('gestao:estabelecimentos'))

@transaction.atomic    
def adicionar_profissional(request, pk):
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


def coordenadores_sus(request):
    title = 'Coordenadores SUS'
    coordenadores_sus = CoordenadorSus.objects.all()
    return render(request, 'gestao/coordenadores_sus.html', locals())


def adicionar_coordenador_sus(request):
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

def dashboard(request):
    return render(request, 'dashboard.html', locals())

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')
