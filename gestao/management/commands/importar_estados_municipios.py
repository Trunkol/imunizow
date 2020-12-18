import pandas
from django.core.management.base import BaseCommand
from gestao.models import Municipio, Estado
from django.conf import settings
from django.db import transaction

def read_csv(filename, delimiter, **args):
    return pandas.read_csv(filename, sep=delimiter, **args)

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = f"{settings.BASE_DIR}/gestao/fixtures/municipios_ibge.csv"
        dados_estados_municipios = read_csv(file_path, ',')
        estados_set = set()

        for i, row in dados_estados_municipios.iterrows():
            estados_set.add((row['UF'], row['Nome_UF']))

        for x in estados_set:
            Estado.objects.create(codigo=x[0], nome=x[1])

        estados = Estado.objects.in_bulk(field_name='codigo')
        cidades = []

        for i, row in dados_estados_municipios.iterrows():
            cidades.append(
                Municipio(codigo=row['Codigo_Municipio'],
                            nome=row['Nome_Municipio'],
                            estado=estados[str(row['UF'])])
            )

        Municipio.objects.bulk_create(cidades)		