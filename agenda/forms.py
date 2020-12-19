from django import forms
from django.db import transaction
from django.urls import reverse
from django_select2.forms import ModelSelect2MultipleWidget
from agenda.models import Campanha
from gestao.models import Estabelecimento

class CampanhaForm(forms.ModelForm):
    titulo = forms.CharField(label=u'Titulo', widget=forms.TextInput(attrs={'placeholder': 'titulo da campanha', 'class': "form-control"}))
    data_inicio = forms.DateField(label=u'Data de Início', input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                    attrs={'placeholder': 'dia/mês/ano', 'class': 'form-control', 
                                            'data-toggle': "input-mask", 'data-mask-format': "00/00/0000"}))
    data_fim = forms.DateField(label=u'Data de Fim', input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                    attrs={'placeholder': 'dia/mês/ano', 'class': 'form-control', 
                                            'data-toggle': "input-mask", 'data-mask-format': "00/00/0000"}))
    estabelecimentos = forms.ModelMultipleChoiceField(label='Estabelecimentos', queryset=Estabelecimento.objects, required=True,
                            widget=ModelSelect2MultipleWidget(model=Estabelecimento, 
                                                search_fields=['nome__icontains', 'cnes__icontains'], 
                                                attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                        "data-placeholder": "Busque e selecione o(s) estabelecimentos"}))
    class Meta:
        model = Campanha
        exclude = ()    

    def clean(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_fim = self.cleaned_data.get('data_fim')        
        if data_inicio > data_fim:
            self.add_error('data_fim', 'A data de finalização não pode ser antes da inicial')


