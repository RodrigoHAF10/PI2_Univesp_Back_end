from django.contrib import admin
from .models import Usuario
from django.contrib.auth.models import User

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['register_prefeitura', 'coluna_1234']  # Usuário: Prefeitura1 e senha: 1234

# Verifica se o usuário 'prefeitura1' já existe antes de criá-lo
if not User.objects.filter(username='prefeitura1').exists():
    User.objects.create_user('prefeitura1', password='1234')
