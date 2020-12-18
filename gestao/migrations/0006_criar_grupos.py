# Generated by Django 3.1.1 on 2020-12-18 17:09

from django.db import migrations
from django.contrib.auth.models import Group

def carregar_grupos(apps, schema_editor):
    Group.objects.get_or_create(name='Coordenador SUS')
    Group.objects.get_or_create(name='Paciente')
    Group.objects.get_or_create(name='Profissional de Saúde')

class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0005_coordenadorsus'),
    ]

    operations = [
        migrations.RunPython(carregar_grupos)
    ]