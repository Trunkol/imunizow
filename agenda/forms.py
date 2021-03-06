from django import forms
from django.db import transaction
from django.urls import reverse
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget, Select2Widget
from agenda.models import Campanha, Estoque, Agendamento, Vacina, VacinaPrivada
from gestao.models import Estabelecimento, Paciente
from django.db.models import Sum, Max, Count
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
                                                "data-placeholder": "Busque e selecione uma campanha"}))
    estabelecimento = forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects, required=False,
                                        widget=ModelSelect2Widget(model=Estabelecimento, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione um estabelecimento"}))
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
        exclude = ('status', 'paciente', 'data_aplicacao', 'estoque')    

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
            estoque_disponivel = Estoque.objects.filter(estabelecimento=self.estabelecimento, campanha=self.campanha).aggregate(qtd=Sum('quantidade'))['qtd']
            self.add_error('quantidade', 'O número de agendamentos supera as vacinas disponíveis para este estabelecimento: {}'.format(estoque_disponivel or 0))

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
        
        
class AgendarVacinacaoEstabelecimentoForm(forms.Form):
    estabelecimento = forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects, required=False,
                                        widget=ModelSelect2Widget(model=Estabelecimento, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione um estabelecimento"}))
    campanha = forms.ModelChoiceField(label='Campanha', queryset=Campanha.objects, required=False,
                                        widget=ModelSelect2Widget(model=Campanha, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma campanha"}))
    
    def __init__(self, *args, **kwargs):
        self.campanha = kwargs.pop('campanha', None)
        super(AgendarVacinacaoEstabelecimentoForm, self).__init__(*args,**kwargs)
    
        if self.campanha:
            self.fields['campanha'].initial = self.campanha
            self.fields['campanha'].disabled = True
            
            estabelecimentos_com_agendamento = Agendamento.objects.filter(campanha=self.campanha, 
                                                                            status=Agendamento.DISPONIVEL)\
                                                                        .values_list('estabelecimento', flat=True)
            id_estabs_disponiveis = set(estabelecimentos_com_agendamento)        
            self.fields['estabelecimento'].queryset = Estabelecimento.objects.filter(pk__in=id_estabs_disponiveis)

class AgendarVacinacaoDataForm(forms.Form):
    data = forms.ChoiceField(label='Data de Vacinação', choices=[], widget=Select2Widget(attrs={'class': "form-control",
                                                                                      "data-placeholder": "Selecione a data disponível"}))

    campanha = forms.ModelChoiceField(label='Campanha', queryset=Campanha.objects, required=False,
                                        widget=ModelSelect2Widget(model=Campanha, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))
    estabelecimento = forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects, required=False,
                                        widget=ModelSelect2Widget(model=Estabelecimento, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))

    def __init__(self, *args, **kwargs):
        self.estabelecimento = kwargs.pop('estabelecimento', None)
        self.campanha = kwargs.pop('campanha', None)
        self.paciente = kwargs.pop('paciente', None)
        super(AgendarVacinacaoDataForm, self).__init__(*args,**kwargs)
        
        if self.estabelecimento:
            self.fields['estabelecimento'].initial = self.estabelecimento
            self.fields['estabelecimento'].disabled = True
        
        if self.campanha:
            self.fields['campanha'].initial = self.campanha
            self.fields['campanha'].disabled = True

        agendamentos = Agendamento.objects.filter(campanha=self.campanha, 
                                                    status=Agendamento.DISPONIVEL, 
                                                    estabelecimento=self.estabelecimento).order_by('data')\
                                            .values_list('data', flat=True)
        if agendamentos:
            agendamentos = set(agendamentos)
            data_agendamento_choices = []
            for dia in agendamentos:
                data_agendamento_choices.append((dia, dia.strftime('%d/%m/%Y')))
            self.fields['data'].choices = set(data_agendamento_choices)

    @transaction.atomic
    def save(self):
        self.data = self.cleaned_data.get('data')
        agendamento = Agendamento.objects.filter(campanha=self.campanha, 
                                            status=Agendamento.DISPONIVEL, 
                                            estabelecimento=self.estabelecimento, 
                                            data=self.data).order_by('pk').first()
        agendamento.paciente = self.paciente
        agendamento.status = Agendamento.OCUPADO
        agendamento.save()


class ConfirmacaoVacinaForm(forms.Form):
    estoque = forms.ModelChoiceField(label='Lote de Vacinação', queryset=Estoque.objects, required=True,
                                        widget=ModelSelect2Widget(model=Estoque, search_fields=['lote__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione um lote"}))
    campanha = forms.ModelChoiceField(label='Campanha', queryset=Campanha.objects,
                                        widget=ModelSelect2Widget(model=Campanha, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))
    estabelecimento = forms.ModelChoiceField(label='Estabelecimento', queryset=Estabelecimento.objects,
                                        widget=ModelSelect2Widget(model=Estabelecimento, search_fields=['nome__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e selecione uma empresa"}))

    def __init__(self, *args, **kwargs):
        self.agendamento = kwargs.pop('agendamento', None)
        super(ConfirmacaoVacinaForm, self).__init__(*args,**kwargs)
        
        if self.agendamento:
            self.fields['estabelecimento'].initial = self.agendamento.estabelecimento
            self.fields['estabelecimento'].disabled = True
        
            self.fields['campanha'].initial = self.agendamento.campanha
            self.fields['campanha'].disabled = True

            self.fields['estoque'].queryset = Estoque.objects.filter(campanha=self.agendamento.campanha)

    @transaction.atomic
    def save(self):
        self.agendamento.estoque = self.cleaned_data.get('estoque')
        self.agendamento.status = Agendamento.APLICADA
        self.agendamento.data_aplicacao = datetime.datetime.now()
        self.agendamento.save()
        Vacina.objects.create(estabelecimento=self.agendamento.estabelecimento,
                                campanha=self.agendamento.campanha, paciente=self.agendamento.paciente,
                                estoque=self.cleaned_data.get('estoque'), agendamento=self.agendamento)


class VacinaPrivadaForm(forms.ModelForm):
    descricao = forms.CharField(label='Nome da Vacina', max_length=20, 
                            widget=forms.TextInput(attrs={'placeholder': 'Descrição da vacina aplicada', 'class': "form-control"}))
    estabelecimento = forms.CharField(label='Estabelecimento', max_length=20, 
                            widget=forms.TextInput(attrs={'placeholder': 'Estabelecimento de saúde', 'class': "form-control"}))
    data_vacinacao = forms.DateField(label=u'Data da vacinação', input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                    attrs={'placeholder': 'dia/mês/ano', 'class': 'form-control', 
                                            'data-toggle': "input-mask", 'data-mask-format': "00/00/0000"}))
    lote = forms.CharField(label='Lote da Vacina', max_length=20, 
                            widget=forms.TextInput(attrs={'placeholder': 'código do lote de vacinação', 'class': "form-control"}))
    paciente = forms.ModelChoiceField(label='Paciente', queryset=Paciente.objects, required=True,
                                        widget=ModelSelect2Widget(model=Paciente, search_fields=['lote__icontains'],
                                        attrs={'class': "form-control", "data-minimum-input-length": "0", 
                                                "data-placeholder": "Busque e Selecione um paciente"}))
    class Meta:
        model = VacinaPrivada
        exclude = ()

    def __init__(self, *args, **kwargs):
        self.paciente = kwargs.pop('paciente', None)
        super(VacinaPrivadaForm, self).__init__(*args,**kwargs)

        if self.paciente:
            self.fields['paciente'].initial = self.paciente
            self.fields['paciente'].disabled = True