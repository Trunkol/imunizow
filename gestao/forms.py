from django import forms
from django.db import transaction
from django.urls import reverse
from django_select2.forms import Select2MultipleWidget, ModelSelect2Widget, Select2Widget, ModelSelect2MultipleWidget
from gestao.models import PessoaFisica, Municipio, ProfissionalSaude, Estabelecimento

class PessoaFisicaForm(forms.ModelForm):
    cpf = forms.CharField(label=u'CPF', widget=forms.TextInput(attrs={'placeholder': '00.000.000-00', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "000.000.000-00"}))
    nome = forms.CharField(label='Nome Completo', widget=forms.TextInput(attrs={'placeholder': 'nome completo', 'class': "form-control"}))
    email = forms.CharField(label=u'Email', required=True, widget=forms.TextInput(attrs={'placeholder': 'email@email.com', 'class': "form-control"}))
    data_nascimento = forms.DateField(label=u'Data de Nascimento', input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',
                                                                                     attrs={'placeholder': 'dia/mês/ano', 'class': 'form-control', 'data-toggle': "input-mask", 'data-mask-format': "00/00/0000"}))
    sexo = forms.ChoiceField(label='Sexo', choices=PessoaFisica.SEXO_FORM_CHOICES,  widget=Select2Widget(attrs={'class': "form-control", 'data-placeholder': 'Selecione o sexo'}))
    celulares = forms.CharField(label='Celular', required=False, widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "(00) 00000-0000"}))
    telefones = forms.CharField(label='Fixo', required=False, widget=forms.TextInput(attrs={'placeholder': '(00) 0000-0000', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "(00) 0000-0000"}))

    cep = forms.CharField(label='CEP', max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': '00000-000', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "00000-000"}))
    logradouro = forms.CharField(label='Logradouro', max_length=80, required=False, widget=forms.TextInput(attrs={'placeholder': 'logradouro', 'class': "form-control"}))
    numero = forms.CharField(label=u'Número', max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': '000', 'class': "form-control"}))
    complemento = forms.CharField(label=u'Complemento', max_length=80, required=False, widget=forms.TextInput(attrs={'placeholder': 'apartamento 23', 'class': "form-control"}))
    bairro = forms.CharField(label=u'Bairro', max_length=80, required=False, widget=forms.TextInput(attrs={'placeholder': 'bairro', 'class': "form-control"}))
    municipio = forms.ModelChoiceField(label='Município', queryset=Municipio.objects, required=True,
                                       widget=ModelSelect2Widget(model=Municipio, search_fields=['nome__icontains'],
                                                                 attrs={'class': "form-control", "data-minimum-input-length": "0", "data-placeholder": "Busque e selecione um município"}))

    class Meta:
        model = PessoaFisica
        exclude = ('user',)


class EstabelecimentoForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'nome', 'class': "form-control"}))
    cnes = forms.CharField(label='CNES', widget=forms.TextInput(attrs={'placeholder': 'cnes', 'class': "form-control"}))
    razao_social = forms.CharField(label='Razão Social', required=False,widget=forms.TextInput(attrs={'placeholder': 'razão social', 'class': "form-control"}))
    cnpj = forms.CharField(label='CNPJ', required=False,widget=forms.TextInput(attrs={'placeholder': 'cnpj', 'class': "form-control"}))
    cep = forms.CharField(label='CEP', max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': '00000-000', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "00000-000"}))
    logradouro = forms.CharField(label='Logradouro', max_length=80, required=False, widget=forms.TextInput(attrs={'placeholder': 'logradouro', 'class': "form-control"}))
    num_endereco = forms.CharField(label=u'Número', max_length=10, required=False, widget=forms.TextInput(attrs={'placeholder': '000', 'class': "form-control"}))
    complemento = forms.CharField(label=u'Complemento', max_length=80, required=False, widget=forms.TextInput(attrs={'placeholder': 'apartamento 23', 'class': "form-control"}))
    bairro = forms.CharField(label=u'Bairro', max_length=80, required=False, widget=forms.TextInput(attrs={'placeholder': 'bairro', 'class': "form-control"}))
    municipio = forms.ModelChoiceField(label='Município', queryset=Municipio.objects, required=True,
                                       widget=ModelSelect2Widget(model=Municipio, search_fields=['nome__icontains'],
                                                                 attrs={'class': "form-control", "data-minimum-input-length": "0", "data-placeholder": "Busque e selecione um município"}))
    celular = forms.CharField(label='Celular', required=False, widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "(00) 00000-0000"}))
    telefone = forms.CharField(label='Fixo', required=False, widget=forms.TextInput(attrs={'placeholder': '(00) 0000-0000', 'class': "form-control", 'data-toggle': "input-mask", 'data-mask-format': "(00) 0000-0000"}))
    email = forms.CharField(label=u'Email', required=False, widget=forms.TextInput(attrs={'placeholder': 'email@email.com', 'class': "form-control"}))
    ativo = forms.BooleanField(label='Ativo', widget=forms.NullBooleanSelect(attrs={'data-placeholder': 'Selecione', 'class': 'form-control'}), required=False)

    class Meta:
        model = Estabelecimento
        fields = ( 'nome', 'cnes', 'razao_social', 'cnpj','email', 
                    'celular', 'telefone',  'cep', 'logradouro', 'num_endereco', 
                    'complemento', 'bairro',  'municipio', 'ativo')
