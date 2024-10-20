# Generated by Django 5.0.4 on 2024-05-26 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_solicitacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='tipo_solicitacao',
            field=models.CharField(choices=[('manutencao', 'Manutenção'), ('outra_opcao', 'Melhoria'), ('mais_uma_opcao', 'Reclamação')], default='manutencao', max_length=20),
        ),
    ]
