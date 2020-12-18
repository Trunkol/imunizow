import pandas
from django.core.management.base import BaseCommand
from gestao.models import Municipio, Estabelecimento
from django.conf import settings

def read_csv(filename, delimiter, **args):
    return pandas.read_csv(filename, sep=delimiter, **args)

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = f"{settings.BASE_DIR}/gestao/fixtures/estabelecimentos_saude.csv"
        estabelecimentos_saude = read_csv(file_path, ',', dtype={'NU_CNPJ': str})

        municipios = Municipio.objects.in_bulk(field_name='codigo')
        
        unidades = []
        for i, row in estabelecimentos_saude.iterrows():
            unidades.append(
                Estabelecimento(cnes=row['CO_CNES'], nome = row['NO_FANTASIA'],
                                razao_social = row['NO_RAZAO_SOCIAL'],
                                municipio=municipios[str(row['CO_MUNICIPIO_GESTOR'])],
                                logradouro=row['NO_LOGRADOURO'],
                                num_endereco=row['NU_ENDERECO'],
                                complemento=row['NO_COMPLEMENTO'],
                                bairro=row['NO_BAIRRO'], email=row['NO_EMAIL'],
                                cep=row['CO_CEP'], telefone=row['NU_TELEFONE'],
                                latitude=row['NU_LATITUDE'], longitude = row['NU_LONGITUDE'])
            )

        Estabelecimento.objects.bulk_create(unidades)		