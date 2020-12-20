from django import forms
from django.db import transaction
from django.urls import reverse
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget, Select2Widget
from agenda.models import Campanha, Estoque, Agendamento
from gestao.models import Estabelecimento
import datetime

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


class EstoqueForm(forms.ModelForm):
    quantidade = forms.IntegerField(label='Quantidade de Vacinas', widget=forms.NumberInput(attrs={'class': "form-control", 'min': 0}))
    campanha = forms.ModelChoiceField(label='Campanha', queryset=Campanha.objects, required=False,
                                        widget=ModelSelect2Widget(model=Campanha, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))
    estabelecimento = forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects, required=False,
                                        widget=ModelSelect2Widget(model=Estabelecimento, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))
    lote = forms.CharField(label='Lote de Vacinas', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'código de Identificação do Lote', 'class': "form-control"}))
    
    class Meta:
        model = Estoque
        exclude = ()    

    def __init__(self, *args, **kwargs):
        self.estabelecimento = kwargs.pop('estabelecimento', None)
        self.campanha = kwargs.pop('campanha', None)
        super(EstoqueForm, self).__init__(*args,**kwargs)
        
        if self.estabelecimento:
            self.fields['estabelecimento'].initial = self.estabelecimento
            self.fields['estabelecimento'].disabled = True
        
        if self.campanha:
            self.fields['campanha'].initial = self.campanha
            self.fields['campanha'].disabled = True

    def clean(self):
        quantidade = self.cleaned_data.get('quantidade')
        if int(quantidade) < 0:
            self.add_error('quantidade', 'A quantidade não pode ser menor que zero')


class AgendamentoForm(forms.ModelForm):
    data = forms.DateField(label=u'Data de Início', input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                    attrs={'placeholder': 'dia/mês/ano', 'class': 'form-control', 
                                            'data-toggle': "input-mask", 'data-mask-format': "00/00/0000"}))
    quantidade = forms.IntegerField(label='Quantidade de Vacinas', widget=forms.NumberInput(attrs={'class': "form-control", 'min': 0}))
    campanha = forms.ModelChoiceField(label='Campanha', queryset=Campanha.objects, required=False,
                                        widget=ModelSelect2Widget(model=Campanha, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))
    estabelecimento = forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects, required=False,
                                        widget=ModelSelect2Widget(model=Estabelecimento, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))

    class Meta:
        model = Agendamento
        exclude = ('status', 'paciente')    

    def __init__(self, *args, **kwargs):
        self.estabelecimento = kwargs.pop('estabelecimento', None)
        self.campanha = kwargs.pop('campanha', None)
        super(AgendamentoForm, self).__init__(*args,**kwargs)
        
        if self.estabelecimento:
            self.fields['estabelecimento'].initial = self.estabelecimento
            self.fields['estabelecimento'].disabled = True
        
        if self.campanha:
            self.fields['campanha'].initial = self.campanha
            self.fields['campanha'].disabled = True

    def clean(self):
        quantidade = self.cleaned_data.get('quantidade')
        data = self.cleaned_data.get('data')
        campanha = self.cleaned_data.get('campanha')
        if int(quantidade) < 0:
            self.add_error('quantidade', 'A quantidade não pode ser menor que zero')

        if int(quantidade) > campanha.estoque_disponivel():
            self.add_error('quantidade', 'O número de agendamentos supera as vacinas disponíveis para este estabelecimento: {}'.format(campanha.estoque_disponivel()))

        if data < datetime.date(2020, 12, 10):
            self.add_error('data', 'A data não pode ser inferior a 12/2020')
    
    def save(self):
        agendamentos = []
        quantidade_agendamentos = self.cleaned_data.get('quantidade')
        for x in range(quantidade_agendamentos):
            agendamentos.append(
                Agendamento(status=Agendamento.DISPONIVEL, data=self.cleaned_data.get('data'), 
                            campanha=self.cleaned_data.get('campanha'), 
                            estabelecimento=self.cleaned_data.get('estabelecimento'))
            )        
        Agendamento.objects.bulk_create(agendamentos)
        
        

