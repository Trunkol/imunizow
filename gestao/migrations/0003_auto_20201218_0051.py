# Generated by Django 3.1.1 on 2020-12-18 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0002_auto_20201217_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfissionalSaude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProfissionalSaudeEstabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField()),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao.estabelecimento')),
                ('profissional_saude', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao.profissionalsaude')),
            ],
        ),
        migrations.AddField(
            model_name='profissionalsaude',
            name='estabelecimentos',
            field=models.ManyToManyField(through='gestao.ProfissionalSaudeEstabelecimento', to='gestao.Estabelecimento'),
        ),
        migrations.AddField(
            model_name='profissionalsaude',
            name='pessoa_fisica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestao.pessoafisica'),
        ),
    ]
