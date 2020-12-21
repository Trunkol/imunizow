from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

@login_required
def index(request):
    if request.user.eh_coordenador_sus():
        return redirect('gestao:dashboard_geral')
    
    if request.user.eh_profissional_saude():
        return redirect('gestao:detalhar_estabelecimento', pk=request.user.profissional_saude().estabelecimento.pk)

    if request.user.eh_paciente():
        return redirect('agenda:index')
    
    return redirect('agenda:autocadastro')