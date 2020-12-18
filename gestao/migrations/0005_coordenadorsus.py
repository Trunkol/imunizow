# Generated by Django 3.1.1 on 2020-12-18 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0004_auto_20201218_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoordenadorSus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('pessoa_fisica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao.pessoafisica')),
            ],
        ),
    ]
