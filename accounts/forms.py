from django import forms
from .models import Usuario
from .models import Solicitacao          

# Log in prefeitura

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['register_prefeitura', 'coluna_1234']
        widgets = {
            'coluna_1234': forms.PasswordInput(),
        }

# Formulário munícipe
'''''
class SolicitacaoForm(forms.ModelForm):
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'maxlength': '50'}))

    class Meta:
        model = Solicitacao
        fields = ['nome', 'endereco', 'email', 'mensagem', 'imagem', 'tipo_solicitacao', 'prioridade']   
'''

class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['nome', 'endereco', 'email', 'mensagem', 'imagem', 'tipo_solicitacao', 'prioridade']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo',
                'required': 'required'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da rua e número',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu email',
                'required': 'required'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Escreva aqui',
                'required': 'required'
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'tipo_solicitacao': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'prioridade': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
        }
