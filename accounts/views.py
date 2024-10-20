from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Usuario, Solicitacao
from .forms import SolicitacaoForm
from rest_framework import viewsets
from .serializers import SolicitacaoSerializer
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status


# Para lidar com as solicitações
@api_view(['POST'])
def create_solicitacao(request):
    if request.method == 'POST':
        print(f"Dados recebidos: {request.data}")  # Adicione isso para depuração
        serializer = SolicitacaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"Erros de validação: {serializer.errors}")  # Adicione isso para depuração
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para API REST de Solicitações
class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer

# Função para registro de munícipe
@csrf_exempt
def register_municipe(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=email).exists():
                raise ValidationError("Este e-mail já está em uso.")
            else:
                User.objects.create_user(username=email, password=password)
                return redirect('login_municipe')
        except ValidationError as e:
            context['error'] = str(e)
    return render(request, 'register_municipe.html', context)

# Função de login do munícipe
def login_municipe_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password) 
        if user is not None:
            login(request, user)
            return redirect('painel_solicitacoes_municipe')  # Redireciona para o painel de solicitações
    return render(request, 'login_municipe.html')

# Função de login da prefeitura
def login_prefeitura(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Melhor prática: verificar se o usuário pertence a um grupo específico da prefeitura
            if user.username == 'prefeitura1':
                login(request, user)
                return redirect('painel_solicitacoes_prefeitura')
            else:
                return render(request, 'login_prefeitura.html', {'error': 'Usuário ou senha incorretos'})
        else:
            return render(request, 'login_prefeitura.html', {'error': 'Usuário ou senha incorretos'})
    return render(request, 'login_prefeitura.html')

# Painel de solicitações do munícipe WEB
def painel_solicitacoes_municipe(request):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, request.FILES)
        if form.is_valid():
            nova_solicitacao = form.save()
            # Redireciona para a página de sucesso com o ID da solicitação
            return redirect('solicitacoes_municipe_sucesso', id=nova_solicitacao.id)
    else:
        form = SolicitacaoForm()
    return render(request, 'painel_solicitacoes_municipe.html', {'form': form})

# Painel de solicitações do munícipe APP
def solicitacoes_municipe_sucesso(request, id):
    solicitacao = get_object_or_404(Solicitacao, id=id)
    return render(request, 'solicitacoes_municipe_sucesso.html', {'solicitacao': solicitacao})

# Painel de solicitações da prefeitura
def painel_solicitacoes_prefeitura(request):
    solicitacoes = Solicitacao.objects.all()
    return render(request, 'painel_solicitacoes_prefeitura.html', {'solicitacoes': solicitacoes})

# Atualizar status da solicitação
def atualizar_status(request, id, status):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.status = status
    solicitacao.save()
    return redirect('painel_solicitacoes_prefeitura')

# Atualizar prioridade da solicitação
def atualizar_prioridade(request, id, prioridade):
    solicitacao = Solicitacao.objects.get(id=id)
    solicitacao.prioridade = prioridade
    solicitacao.save()
    return redirect('painel_solicitacoes_prefeitura')

# Exibir página de sucesso para o munícipe após enviar solicitação
def solicitacoes_municipe_sucesso(request, id):
    solicitacao = get_object_or_404(Solicitacao, id=id)
    return render(request, 'solicitacoes_municipe_sucesso.html', {'solicitacao': solicitacao})

# Função para o reset de senha (personalizado)
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request, 'password/password_reset.html', {"password_reset_form": password_reset_form})
