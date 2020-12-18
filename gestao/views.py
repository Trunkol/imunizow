from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import F, Sum, Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from gestao.models import Estabelecimento
from django.shortcuts import render
from gestao.forms import EstabelecimentoForm


# Create your views here.
def estabelecimentos(request):
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'gestao/estabelecimentos.html', locals())

def detalhar_estabelecimento(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    return render(request, 'gestao/detalhar_estabelecimento.html', locals())

def editar_estabelecimento(request, pk):
    estabelecimento = get_object_or_404(Estabelecimento, pk=pk)
    form = EstabelecimentoForm(request.POST or None, instance=estabelecimento)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('gestao:detalhar_estabelecimento', args=(pk,) ))
    return render(request, 'gestao/form_base.html', locals())