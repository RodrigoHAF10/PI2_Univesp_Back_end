from django.db import models

# Create your models here.


class Usuario(models.Model):
    register_prefeitura = models.CharField(max_length=50)
    coluna_1234 = models.CharField(max_length=50)
    

# solicitacoes/models.py


class Solicitacao(models.Model):
    #id_Solicitacoes = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255)
    email = models.EmailField()
    mensagem = models.TextField()
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('em aberto', 'Em Aberto'),
            ('pendente', 'Pendente'),
            ('finalizado', 'Finalizado')
        ],
        default='em aberto'
    )
    data_abertura = models.DateTimeField(auto_now_add=True)
    tipo_solicitacao = models.CharField(
        max_length=20,
        choices=[
            ('manutencao', 'Manutenção'),
            ('outra_opcao', 'Melhoria'),
            ('mais_uma_opcao', 'Reclamação')
        ],
        default='manutencao'
    )
    prioridade = models.CharField(
        max_length=20,
        choices=[
            ('minima', 'Mínima'),
            ('maxima', 'Máxima')
        ],
        default='minima'
    )

    class Meta:
        db_table = 'dados_solicitacoes'

    def __str__(self):
        return f"{self.nome} - {self.endereco}"
