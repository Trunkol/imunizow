from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Estado(models.Model):
    nome = models.CharField(u'Nome', max_length=80)
    codigo = models.CharField(u'Código IBGE', max_length=7, unique=True)

class Municipio(models.Model):
    codigo = models.CharField(u'Código IBGE', max_length=7, unique=True)
    nome = models.CharField(u'Nome', max_length=80)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('nome', )

    def __str__(self):
        return u'%s / %s' % (self.nome, self.estado.nome)

class PessoaFisica(models.Model):
    SEXO_MASCULINO  = u'M'
    SEXO_FEMININO = u'F'
    SEXO_NAO_INFORMADO = u'N'
    SEXO_CHOICES = (
                        (SEXO_MASCULINO, u'Masculino'),
                        (SEXO_FEMININO, u'Feminino'),
                        (SEXO_NAO_INFORMADO, u'Não Informado')
                    )
    SEXO_FORM_CHOICES = (
                        ('', ''),
                        (SEXO_MASCULINO, u'Masculino'),
                        (SEXO_FEMININO, u'Feminino'),
                    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(u'CPF',max_length=15, help_text=u'Digite o CPF sem pontos ou traços.', null=True, unique=True)
    sexo = models.CharField(u'Sexo', max_length=1, choices=SEXO_CHOICES, default=SEXO_NAO_INFORMADO)
    data_nascimento = models.DateField(u'Data de Nascimento', null=True)
    telefones = models.CharField(u'Telefones', max_length=60, null=True, blank=True)
    celulares = models.CharField(u'Celulares', max_length=60, null=True, blank=True)
    email = models.CharField(u'Email', max_length=80, null=True, blank=True)
    logradouro = models.CharField(u'Logradouro', max_length=80, null=True, blank=True)
    numero = models.CharField(u'Número', max_length=10, null=True, blank=True)
    complemento = models.CharField(u'Complemento', max_length=80, null=True, blank=True)
    bairro = models.CharField(u'Bairro', max_length=80, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, null=True, blank=True, on_delete=models.CASCADE)
    cep = models.CharField(u'CEP', null=True, blank=True, max_length=15)
    
    class Meta:
        verbose_name = u'Pessoa Fisica'

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        if self.data_nascimento:
            return get_age(self.data_nascimento)

    def get_endereco(self):
        texto = u''
        if self.logradouro:
            texto = texto + self.logradouro

        if self.numero:
            texto = texto + ', '+self.numero

        if self.complemento:
            texto = texto + ' - '+self.complemento

        if self.bairro:
            texto = texto + '. '+self.bairro

        if self.cep:
            texto = texto + '. CEP: '+self.cep +'. '

        if self.municipio:
            texto = texto + ' ' + self.municipio.get_sigla_estado()

        return texto


class Paciente(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)
    cartao_sus = models.CharField(u'Cartão Sus', max_length=15, null=True, blank=True)
    
    class Meta:
        verbose_name = u'Paciente'
        verbose_name_plural = u'Pacientes'
        unique_together = ('pessoa_fisica', 'cartao_sus')

    def __str__(self):
        return self.pessoa_fisica.nome

    @property
    def idade(self):
        return self.pessoa_fisica.idade

class Estabelecimento(models.Model):
    cnes = models.CharField(max_length=12, verbose_name=u'Código CNES', unique=True)
    nome = models.CharField(max_length=60)
    razao_social = models.CharField(max_length=60, verbose_name=u'Razão Social', null=True)
    cnpj = models.CharField(max_length=255, verbose_name=u'CNPJ', null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=60, verbose_name=u'Logradouro', null=True, blank=True)
    num_endereco = models.CharField(max_length=10, verbose_name=u'Número', null=True, blank=True)
    cep = models.CharField(max_length=9, verbose_name=u'CEP', null=True, blank=True)
    telefone = models.CharField(max_length=40, verbose_name=u'Telefone', null=True, blank=True)
    celular = models.CharField(max_length=40, verbose_name=u'Celular', null=True, blank=True)
    email = models.CharField(max_length=100, verbose_name=u'Email', null=True, blank=True)
    complemento = models.CharField(max_length=60, verbose_name=u'Complemento', null=True, blank=True)
    bairro = models.CharField(max_length=60, verbose_name=u'Bairro', null=True, blank=True)
    data_ultima_atualizacao = models.DateTimeField(u'Data da última atualização', null=True)
    ativo = models.BooleanField(verbose_name=u'Ativo',default=True)
    latitude = models.CharField('Latitude', max_length=255, null=True, blank=True)
    longitude = models.CharField('Longitude', max_length=255, null=True, blank=True)
    prestador = models.BooleanField(verbose_name=u'Prestador', default=False)
    
    class Meta:
        verbose_name = u'Estabelecimento de Saúde'
        verbose_name_plural = u'Estabelecimentos de Saúde'
        ordering = ['nome', 'municipio']

    def __str__(self):
        return u'%s (CNES: %s)' % (self.nome, self.cnes)

    def leitos_disponiveis(self):
        return self.leitos.filter(ativo=True, situacao=Leito.DISPONIVEL)

    def get_endereco(self):
        texto = u''
        if self.logradouro:
            texto = texto + self.logradouro

        if self.num_endereco:
            texto = texto + ', '+self.num_endereco

        if self.complemento:
            texto = texto + ' - '+self.complemento

        if self.bairro:
            texto = texto + '. '+self.bairro

        if self.cep:
            texto = texto + '. CEP: '+self.cep

        if self.municipio:
            texto = f'{texto}, {self.municipio.nome} ({self.municipio.estado.nome.upper()})'

        return texto

class ProfissionalSaude(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    ativo = models.BooleanField(verbose_name=u'Ativo', default=False)
    
    class Meta:
        unique_together = ('pessoa_fisica', 'estabelecimento')

class CoordenadorSus(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, on_delete=models.CASCADE)
    ativo = models.BooleanField(verbose_name=u'Ativo', default=True)

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    def eh_profissional_saude(self):
        return ProfissionalSaude.objects.filter(pessoa_fisica__user=self).exists()
    
    def eh_coordenador_sus(self):
        return CoordenadorSus.objects.filter(pessoa_fisica__user=self).exists()

    def eh_paciente(self):
        return Paciente.objects.filter(pessoa_fisica__user=self).exists()

    def paciente(self):
        if Paciente.objects.filter(pessoa_fisica__user=self).exists():
            return Paciente.objects.filter(pessoa_fisica__user=self).first()
        return None

    def profissional_saude(self):
        if ProfissionalSaude.objects.filter(pessoa_fisica__user=self).exists():
            return ProfissionalSaude.objects.filter(pessoa_fisica__user=self).first()

