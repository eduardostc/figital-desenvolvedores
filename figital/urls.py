from django.urls import path
from . import views
from .views import exportar_inscricoes_csv

urlpatterns = [
    # ==========================================================
    # URLs Públicas
    # ==========================================================
    path('', views.index, name='index'),  # Alterado de 'home' para 'index'
    path('login/', views.login_view, name='login'),

    # URL para o novo formulário de inscrição
    path('desenvolvedores/', views.inscricao_desenvolvedor, name='inscricao_desenvolvedores'),

    # ==========================================================
    # URLs Protegidas (Área Administrativa)
    # ==========================================================
    path('registros/', views.index_autenticado, name='index_autenticado'),
    
    # URLs para gerenciar as inscrições
    path('registros/visualizar/', views.visualizar_inscricoes, name='visualizar_inscricoes'),
    path('registros/editar/<int:registro_id>/', views.editar_inscricao, name='editar_inscricao'),
    path('registros/excluir/<int:registro_id>/', views.excluir_inscricao, name='excluir_inscricao'),
    path('registros/exportar-csv/', views.exportar_inscricoes_csv, name='exportar_inscricoes_csv'),
]
