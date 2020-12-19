from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

@login_required
def index(request):
    if request.user.eh_coordenador_sus():
        return redirect('gestao:dashboard')
    
    if request.user.eh_profissional_saude():
        return redirect('gestao:detalhes_estabelecimento', args=(1))

    if request.user.eh_paciente():
        return redirect('agenda:index')
    
    return redirect('agenda:autocadastro')