from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   # Define rota da API
    path('api/solicitacoes/', views.create_solicitacao, name='create_solicitacao'),

    # Login de munícipe e prefeitura
    path('', views.login_municipe_view, name='login_municipe'),
    path('login_prefeitura/', views.login_prefeitura, name='login_prefeitura'),
    
    # Painéis de solicitações
    path('painel_solicitacoes_municipe/', views.painel_solicitacoes_municipe, name='painel_solicitacoes_municipe'),
    path('painel_solicitacoes_prefeitura/', views.painel_solicitacoes_prefeitura, name='painel_solicitacoes_prefeitura'),
    
    # Atualizações de status e prioridade dos chamados
    path('atualizar_status/<int:id>/<str:status>/', views.atualizar_status, name='atualizar_status'),
    path('atualizar_prioridade/<int:id>/<str:prioridade>/', views.atualizar_prioridade, name='atualizar_prioridade'),
    
    # Sucesso na solicitação
    path('sucesso/<int:id>/', views.solicitacoes_municipe_sucesso, name='solicitacoes_municipe_sucesso'),

    # Registro de munícipe
    path('register_municipe/', views.register_municipe, name='register_municipe'),
    
    # Reset de senha (customizado)
    path('password_reset/', views.password_reset_request, name='password_reset'),

    # Rotas padrão para o reset de senha do Django
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]
