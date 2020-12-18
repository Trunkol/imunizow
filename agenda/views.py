from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from gestao.forms import PessoaFisicaForm
from gestao.models import Paciente, PessoaFisica

# Create your views here.
def index(request):
    pass

@login_required
def autocadastro(request):
    title = 'Autocadastro de Paciente'
    instance = PessoaFisica.objects.filter(cpf=request.user.username).first()
    form = PessoaFisicaForm(request.POST or None, instance=instance)
    if form.is_valid():
        pessoa_fisica = form.save(commit=False)
        user = User.objects.create_user(form.cleaned_data['cpf'].replace('-', '').replace('.', ''), 
                                        pessoa_fisica.email, 
                                        f'{pessoa_fisica.cpf}{pessoa_fisica.nome}')
        pessoa_fisica.user = user
        pessoa_fisica.save()

        prof_saude = ProfissionalSaude.objects.create(pessoa_fisica=pessoa_fisica)

        return HttpResponseRedirect(reverse('agenda:index'))
    return render(request, 'gestao/form_base.html', locals())