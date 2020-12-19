from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from gestao.forms import PessoaFisicaForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from gestao.models import Paciente, PessoaFisica, User
from django.db import transaction
from agenda.forms import CampanhaForm
from agenda.models import Campanha
# Create your views here.
def index(request):
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
