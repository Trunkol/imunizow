from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from gestao.models import PessoaFisica, ProfissionalSaude, CoordenadorSus, Paciente
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

@login_required
def index(request):
    pessoa_fisica = PessoaFisica.objects.filter(user=request.user).first()

    if any((CoordenadorSus.objects.filter(pessoa_fisica=pessoa_fisica, ativo=True).exists(),
            ProfissionalSaude.objects.filter(pessoa_fisica=pessoa_fisica, ativo=True).exists())):
        return redirect('gestao:dashboard')

    if Paciente.objects.filter(pessoa_fisica=pessoa_fisica).exists():
        return redirect('agenda:index')

    raise PermissionDenied
